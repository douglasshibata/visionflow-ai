import redis
import json
import base64
import numpy as np
import cv2
import time
import os

def smoke_test():
    redis_password = os.getenv('REDIS_PASSWORD', None)
    r = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=0,
        password=redis_password
    )

    # Create a dummy frame (white 100x100)
    frame = np.ones((100, 100, 3), dtype=np.uint8) * 255
    _, buffer = cv2.imencode('.jpg', frame)
    frame_b64 = base64.b64encode(buffer).decode('utf-8')

    payload = {
        "cameraId": "test-cam",
        "timestamp": str(int(time.time() * 1000)),
        "data": frame_b64
    }

    print("Publishing test frame...")
    r.publish('visionflow:frames', json.dumps(payload))

    pubsub = r.pubsub()
    pubsub.subscribe('visionflow:results')

    print("Waiting for results...")
    for message in pubsub.listen():
        if message['type'] == 'message':
            print("Received detection results:", message['data'])
            break

if __name__ == "__main__":
    print("Make sure Redis and AI Engine are running before executing this test.")
    # smoke_test() # Commented out as services are not running in background here
