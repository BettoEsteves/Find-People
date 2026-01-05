"""Face alignment module for normalizing face images."""
import cv2
import numpy as np
from typing import Tuple, Dict, Optional
from loguru import logger


class FaceAligner:
    """
    Face alignment to normalize pose and scale.

    This class aligns faces based on eye positions or landmarks for
    consistent processing by downstream models.
    """

    def __init__(self, target_size: Tuple[int, int] = (256, 256)):
        """
        Initialize face aligner.

        Args:
            target_size: Target output size (width, height)
        """
        self.target_size = target_size
        logger.info(f"FaceAligner initialized with target size: {target_size}")

    def align(self, image: np.ndarray, landmarks: Dict[str, Tuple[float, float]]) -> np.ndarray:
        """
        Align face based on landmarks.

        Args:
            image: Input face image
            landmarks: Dictionary of landmark points (e.g., {'left_eye': (x, y), 'right_eye': (x, y)})

        Returns:
            Aligned face image
        """
        if not landmarks or 'left_eye' not in landmarks or 'right_eye' not in landmarks:
            # No landmarks available, just resize
            logger.warning("Landmarks not available for alignment, using simple resize")
            return self._simple_resize(image)

        try:
            return self._align_by_eyes(image, landmarks)
        except Exception as e:
            logger.error(f"Alignment failed: {e}, falling back to simple resize")
            return self._simple_resize(image)

    def _align_by_eyes(self, image: np.ndarray, landmarks: Dict[str, Tuple[float, float]]) -> np.ndarray:
        """
        Align face based on eye positions.

        Args:
            image: Input image
            landmarks: Facial landmarks

        Returns:
            Aligned image
        """
        # Get eye coordinates
        left_eye = landmarks['left_eye']
        right_eye = landmarks['right_eye']

        # Calculate angle between eyes
        dx = right_eye[0] - left_eye[0]
        dy = right_eye[1] - left_eye[1]
        angle = np.degrees(np.arctan2(dy, dx))

        # Calculate center point between eyes
        eyes_center = (
            (left_eye[0] + right_eye[0]) / 2,
            (left_eye[1] + right_eye[1]) / 2
        )

        # Get rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D(eyes_center, angle, scale=1.0)

        # Rotate image
        rotated = cv2.warpAffine(
            image,
            rotation_matrix,
            (image.shape[1], image.shape[0]),
            flags=cv2.INTER_CUBIC
        )

        # Calculate eye distance for scaling
        eye_distance = np.sqrt(dx**2 + dy**2)

        # Define desired eye distance (relative to target size)
        desired_eye_distance = self.target_size[0] * 0.3

        # Calculate scale
        scale = desired_eye_distance / eye_distance if eye_distance > 0 else 1.0

        # Resize image
        new_w = int(rotated.shape[1] * scale)
        new_h = int(rotated.shape[0] * scale)
        scaled = cv2.resize(rotated, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

        # Center crop to target size
        aligned = self._center_crop(scaled, self.target_size)

        return aligned

    def _center_crop(self, image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
        """
        Center crop image to target size.

        Args:
            image: Input image
            target_size: Target (width, height)

        Returns:
            Cropped image
        """
        h, w = image.shape[:2]
        target_w, target_h = target_size

        # If image is smaller than target, pad it
        if w < target_w or h < target_h:
            pad_w = max(0, target_w - w)
            pad_h = max(0, target_h - h)

            image = cv2.copyMakeBorder(
                image,
                pad_h // 2,
                pad_h - pad_h // 2,
                pad_w // 2,
                pad_w - pad_w // 2,
                cv2.BORDER_CONSTANT,
                value=[0, 0, 0]
            )
            h, w = image.shape[:2]

        # Calculate crop coordinates
        start_x = (w - target_w) // 2
        start_y = (h - target_h) // 2

        return image[start_y:start_y + target_h, start_x:start_x + target_w]

    def _simple_resize(self, image: np.ndarray) -> np.ndarray:
        """
        Simple resize without alignment (fallback).

        Args:
            image: Input image

        Returns:
            Resized image
        """
        return cv2.resize(image, self.target_size, interpolation=cv2.INTER_CUBIC)

    def align_bbox(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Align face using only bounding box (no landmarks).

        Args:
            image: Input image
            bbox: Bounding box [x1, y1, x2, y2]

        Returns:
            Aligned face image
        """
        x1, y1, x2, y2 = bbox

        # Crop face region
        face = image[y1:y2, x1:x2]

        # Resize to target size
        aligned = cv2.resize(face, self.target_size, interpolation=cv2.INTER_CUBIC)

        return aligned

    def preprocess_for_model(self, image: np.ndarray, normalize: bool = True) -> np.ndarray:
        """
        Preprocess aligned face for model input.

        Args:
            image: Aligned face image
            normalize: Whether to normalize pixel values to [-1, 1]

        Returns:
            Preprocessed image
        """
        # Convert to RGB if needed
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Convert to float
        image = image.astype(np.float32)

        if normalize:
            # Normalize to [-1, 1]
            image = (image / 127.5) - 1.0
        else:
            # Normalize to [0, 1]
            image = image / 255.0

        return image
