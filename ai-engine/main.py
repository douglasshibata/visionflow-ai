import redis
import json
import base64
import cv2
import numpy as np
import os
from vision_processor import VisionProcessor

MAX_FRAME_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_FRAME_WIDTH = 3840
MAX_FRAME_HEIGHT = 2160

class RedisWorker:
    def __init__(self):
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        redis_password = os.getenv('REDIS_PASSWORD', None)

        print(f"Connecting to Redis at {redis_host}:{redis_port}")
        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=0,
            password=redis_password
        )
        self.pubsub = self.r.pubsub()
        self.pubsub.subscribe('visionflow:frames')

        self.processor = VisionProcessor()
        self.batch_size = 4
        self.frame_buffer = []

    def _validate_payload(self, payload):
        """Validate incoming frame payload schema and constraints."""
        if not isinstance(payload, dict):
            raise ValueError("Payload must be a JSON object")

        required_fields = ['cameraId', 'timestamp', 'data']
        for field in required_fields:
            if field not in payload:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(payload['cameraId'], str) or len(payload['cameraId']) > 64:
            raise ValueError("Invalid cameraId: must be a string with max 64 chars")

        if not isinstance(payload['data'], str):
            raise ValueError("Invalid data: must be a base64 string")

        frame_data = base64.b64decode(payload['data'])
        if len(frame_data) > MAX_FRAME_SIZE:
            raise ValueError(f"Frame too large: {len(frame_data)} bytes (max {MAX_FRAME_SIZE})")

        return frame_data

    def _validate_frame(self, frame):
        """Validate decoded frame dimensions."""
        if frame is None:
            raise ValueError("Failed to decode frame")
        h, w = frame.shape[:2]
        if w > MAX_FRAME_WIDTH or h > MAX_FRAME_HEIGHT:
            raise ValueError(f"Frame dimensions {w}x{h} exceed max {MAX_FRAME_WIDTH}x{MAX_FRAME_HEIGHT}")
        return frame

    def run(self):
        print("AI Engine Subscriber running and waiting for frames...")
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                try:
                    payload = json.loads(message['data'])
                    frame_data = self._validate_payload(payload)
                    nparr = np.frombuffer(frame_data, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    frame = self._validate_frame(frame)

                    self.frame_buffer.append({
                        "frame": frame,
                        "cameraId": payload['cameraId'],
                        "timestamp": payload['timestamp']
                    })

                    if len(self.frame_buffer) >= self.batch_size:
                        self.process_current_batch()
                except ValueError as e:
                    print(f"Validation error: {e}")
                except Exception as e:
                    print(f"Error processing message: {e}")

    def process_current_batch(self):
        frames = [item['frame'] for item in self.frame_buffer]
        batch_results = self.processor.process_batch(frames)

        for i, detections in enumerate(batch_results):
            result_payload = {
                "cameraId": self.frame_buffer[i]['cameraId'],
                "timestamp": self.frame_buffer[i]['timestamp'],
                "detections": detections
            }
            for d in detections:
                if d['class'] in ['person', 'helmet', 'vest']:
                    result_payload['alertType'] = 'safety'
                elif d['confidence'] < 0.4:
                    result_payload['alertType'] = 'quality'

            self.r.publish('visionflow:results', json.dumps(result_payload))

        self.frame_buffer = []

if __name__ == "__main__":
    worker = RedisWorker()
    worker.run()
