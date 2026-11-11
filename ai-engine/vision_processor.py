import cv2
import numpy as np
from ultralytics import YOLO
import torch

MAX_BATCH_SIZE = 16

class VisionProcessor:
    def __init__(self, model_path='yolo11n.pt'):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = YOLO(model_path).to(self.device)
        print(f"VisionProcessor initialized on {self.device}")

    def detect_objects(self, frames):
        """
        Processes a batch of frames.
        frames: list of numpy arrays (BGR images)
        """
        results = self.model(frames, conf=0.25, verbose=False)

        batch_detections = []
        for result in results:
            detections = []
            for box in result.boxes:
                detections.append({
                    "class": result.names[int(box.cls[0])],
                    "confidence": float(box.conf[0]),
                    "bbox": box.xyxy[0].tolist()
                })
            batch_detections.append(detections)

        return batch_detections

    def process_batch(self, camera_frames):
        """
        Implements the Batching logic: combines frames into batches
        for YOLO's native batch inference.
        """
        if not isinstance(camera_frames, list):
            raise TypeError("camera_frames must be a list")

        if len(camera_frames) == 0:
            return []

        if len(camera_frames) > MAX_BATCH_SIZE:
            raise ValueError(f"Batch size {len(camera_frames)} exceeds max {MAX_BATCH_SIZE}")

        for i, frame in enumerate(camera_frames):
            if not isinstance(frame, np.ndarray):
                raise TypeError(f"Frame {i} is not a numpy array")
            if frame.ndim != 3 or frame.shape[2] != 3:
                raise ValueError(f"Frame {i} must be a 3-channel BGR image")

        return self.detect_objects(camera_frames)
