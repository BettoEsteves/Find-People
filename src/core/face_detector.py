"""Face detection module using RetinaFace."""
import cv2
import numpy as np
from typing import List, Tuple, Optional
from pathlib import Path
from loguru import logger

try:
    from retinaface import RetinaFace
    RETINAFACE_AVAILABLE = True
except ImportError:
    RETINAFACE_AVAILABLE = False
    logger.warning("RetinaFace not available, falling back to OpenCV Haar Cascade")


class FaceDetector:
    """
    Face detection using RetinaFace or OpenCV Haar Cascade as fallback.

    This class detects faces in images and returns bounding boxes and landmarks.
    """

    def __init__(self, backend: str = "retinaface", confidence_threshold: float = 0.9):
        """
        Initialize face detector.

        Args:
            backend: Detection backend ('retinaface' or 'opencv')
            confidence_threshold: Minimum confidence for detection (0.0-1.0)
        """
        self.backend = backend
        self.confidence_threshold = confidence_threshold

        if backend == "retinaface" and not RETINAFACE_AVAILABLE:
            logger.warning("RetinaFace requested but not available. Using OpenCV.")
            self.backend = "opencv"

        if self.backend == "opencv":
            self._init_opencv_detector()

        logger.info(f"FaceDetector initialized with backend: {self.backend}")

    def _init_opencv_detector(self):
        """Initialize OpenCV Haar Cascade detector."""
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        if self.face_cascade.empty():
            raise RuntimeError("Failed to load OpenCV face cascade")

    def detect(self, image: np.ndarray) -> List[dict]:
        """
        Detect faces in image.

        Args:
            image: Input image as numpy array (BGR format)

        Returns:
            List of face detections, each containing:
                - bbox: [x1, y1, x2, y2]
                - confidence: Detection confidence score
                - landmarks: Facial landmarks (if available)
        """
        if self.backend == "retinaface":
            return self._detect_retinaface(image)
        else:
            return self._detect_opencv(image)

    def _detect_retinaface(self, image: np.ndarray) -> List[dict]:
        """
        Detect faces using RetinaFace.

        Args:
            image: Input image (BGR)

        Returns:
            List of detections
        """
        try:
            # RetinaFace expects RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Detect faces
            detections = RetinaFace.detect_faces(rgb_image)

            if not isinstance(detections, dict):
                return []

            results = []
            for key, detection in detections.items():
                confidence = detection.get('score', 0.0)

                if confidence < self.confidence_threshold:
                    continue

                # Extract bounding box
                facial_area = detection['facial_area']
                bbox = [
                    facial_area[0],  # x1
                    facial_area[1],  # y1
                    facial_area[2],  # x2
                    facial_area[3]   # y2
                ]

                # Extract landmarks
                landmarks = detection.get('landmarks', {})

                results.append({
                    'bbox': bbox,
                    'confidence': confidence,
                    'landmarks': landmarks
                })

            logger.info(f"RetinaFace detected {len(results)} face(s)")
            return results

        except Exception as e:
            logger.error(f"RetinaFace detection failed: {e}")
            return []

    def _detect_opencv(self, image: np.ndarray) -> List[dict]:
        """
        Detect faces using OpenCV Haar Cascade (fallback).

        Args:
            image: Input image (BGR)

        Returns:
            List of detections
        """
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            results = []
            for (x, y, w, h) in faces:
                results.append({
                    'bbox': [x, y, x + w, y + h],
                    'confidence': 1.0,  # OpenCV doesn't provide confidence
                    'landmarks': {}  # OpenCV Haar Cascade doesn't provide landmarks
                })

            logger.info(f"OpenCV detected {len(results)} face(s)")
            return results

        except Exception as e:
            logger.error(f"OpenCV detection failed: {e}")
            return []

    def get_largest_face(self, detections: List[dict]) -> Optional[dict]:
        """
        Get the largest detected face (by bounding box area).

        Args:
            detections: List of face detections

        Returns:
            Largest face detection or None
        """
        if not detections:
            return None

        def bbox_area(det):
            bbox = det['bbox']
            return (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])

        return max(detections, key=bbox_area)

    def crop_face(self, image: np.ndarray, bbox: List[int], padding: float = 0.2) -> np.ndarray:
        """
        Crop face from image with optional padding.

        Args:
            image: Input image
            bbox: Bounding box [x1, y1, x2, y2]
            padding: Padding ratio (0.0-1.0)

        Returns:
            Cropped face image
        """
        x1, y1, x2, y2 = bbox
        h, w = image.shape[:2]

        # Calculate padding
        face_w = x2 - x1
        face_h = y2 - y1
        pad_w = int(face_w * padding)
        pad_h = int(face_h * padding)

        # Apply padding with boundary checks
        x1 = max(0, x1 - pad_w)
        y1 = max(0, y1 - pad_h)
        x2 = min(w, x2 + pad_w)
        y2 = min(h, y2 + pad_h)

        return image[y1:y2, x1:x2]

    def visualize_detections(self, image: np.ndarray, detections: List[dict]) -> np.ndarray:
        """
        Draw bounding boxes and landmarks on image.

        Args:
            image: Input image
            detections: List of face detections

        Returns:
            Image with visualizations
        """
        vis_image = image.copy()

        for det in detections:
            # Draw bounding box
            bbox = det['bbox']
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(vis_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw confidence
            conf = det['confidence']
            label = f"{conf:.2f}"
            cv2.putText(vis_image, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Draw landmarks if available
            landmarks = det.get('landmarks', {})
            for landmark_name, (lx, ly) in landmarks.items():
                cv2.circle(vis_image, (int(lx), int(ly)), 2, (0, 0, 255), -1)

        return vis_image
