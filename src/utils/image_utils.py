"""Image utility functions."""
import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Tuple, Optional
from loguru import logger


class ImageUtils:
    """Utility functions for image processing."""

    @staticmethod
    def load_image(image_path: str) -> Optional[np.ndarray]:
        """
        Load image from file.

        Args:
            image_path: Path to image file

        Returns:
            Image as numpy array (BGR) or None if loading fails
        """
        try:
            image = cv2.imread(str(image_path))
            if image is None:
                logger.error(f"Failed to load image: {image_path}")
                return None
            logger.info(f"Loaded image: {image_path}, shape: {image.shape}")
            return image
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {e}")
            return None

    @staticmethod
    def save_image(image: np.ndarray, output_path: str, quality: int = 95) -> bool:
        """
        Save image to file.

        Args:
            image: Image as numpy array
            output_path: Output file path
            quality: JPEG quality (0-100)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            # Save with quality
            if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
                cv2.imwrite(output_path, image, [cv2.IMWRITE_JPEG_QUALITY, quality])
            else:
                cv2.imwrite(output_path, image)

            logger.info(f"Saved image: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving image {output_path}: {e}")
            return False

    @staticmethod
    def resize_image(
        image: np.ndarray,
        target_size: Tuple[int, int],
        keep_aspect_ratio: bool = True
    ) -> np.ndarray:
        """
        Resize image to target size.

        Args:
            image: Input image
            target_size: Target (width, height)
            keep_aspect_ratio: Whether to maintain aspect ratio

        Returns:
            Resized image
        """
        if keep_aspect_ratio:
            h, w = image.shape[:2]
            target_w, target_h = target_size

            # Calculate scaling factor
            scale = min(target_w / w, target_h / h)

            # Calculate new size
            new_w = int(w * scale)
            new_h = int(h * scale)

            # Resize
            resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

            # Pad to target size if needed
            if new_w < target_w or new_h < target_h:
                pad_w = target_w - new_w
                pad_h = target_h - new_h

                resized = cv2.copyMakeBorder(
                    resized,
                    pad_h // 2,
                    pad_h - pad_h // 2,
                    pad_w // 2,
                    pad_w - pad_w // 2,
                    cv2.BORDER_CONSTANT,
                    value=[0, 0, 0]
                )

            return resized
        else:
            return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)

    @staticmethod
    def validate_image(image_path: str, max_size_mb: int = 10) -> Tuple[bool, str]:
        """
        Validate image file.

        Args:
            image_path: Path to image file
            max_size_mb: Maximum file size in MB

        Returns:
            Tuple of (is_valid, error_message)
        """
        path = Path(image_path)

        # Check if file exists
        if not path.exists():
            return False, "File does not exist"

        # Check file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        if path.suffix.lower() not in valid_extensions:
            return False, f"Invalid file format. Supported: {', '.join(valid_extensions)}"

        # Check file size
        file_size_mb = path.stat().st_size / (1024 * 1024)
        if file_size_mb > max_size_mb:
            return False, f"File too large ({file_size_mb:.2f} MB). Max size: {max_size_mb} MB"

        # Try to load image
        image = cv2.imread(str(path))
        if image is None:
            return False, "Cannot read image file"

        return True, ""

    @staticmethod
    def convert_to_rgb(image: np.ndarray) -> np.ndarray:
        """
        Convert image to RGB format.

        Args:
            image: Input image (any format)

        Returns:
            RGB image
        """
        if len(image.shape) == 2:
            # Grayscale to RGB
            return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            # RGBA to RGB
            return cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        elif image.shape[2] == 3:
            # BGR to RGB
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            return image

    @staticmethod
    def convert_to_bgr(image: np.ndarray) -> np.ndarray:
        """
        Convert image to BGR format (OpenCV default).

        Args:
            image: Input image (any format)

        Returns:
            BGR image
        """
        if len(image.shape) == 2:
            # Grayscale to BGR
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif image.shape[2] == 4:
            # RGBA to BGR
            return cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        elif image.shape[2] == 3:
            # Assume RGB, convert to BGR
            return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        else:
            return image

    @staticmethod
    def create_side_by_side(
        image1: np.ndarray,
        image2: np.ndarray,
        gap: int = 20,
        labels: Tuple[str, str] = None
    ) -> np.ndarray:
        """
        Create side-by-side comparison image.

        Args:
            image1: First image
            image2: Second image
            gap: Gap between images in pixels
            labels: Optional labels for images

        Returns:
            Combined image
        """
        # Ensure same height
        h1, w1 = image1.shape[:2]
        h2, w2 = image2.shape[:2]

        target_h = max(h1, h2)

        # Resize if needed
        if h1 != target_h:
            scale = target_h / h1
            image1 = cv2.resize(image1, (int(w1 * scale), target_h))
            h1, w1 = image1.shape[:2]

        if h2 != target_h:
            scale = target_h / h2
            image2 = cv2.resize(image2, (int(w2 * scale), target_h))
            h2, w2 = image2.shape[:2]

        # Create combined image
        combined_w = w1 + gap + w2
        combined = np.ones((target_h, combined_w, 3), dtype=np.uint8) * 255

        # Place images
        combined[:, :w1] = image1
        combined[:, w1 + gap:] = image2

        # Add labels if provided
        if labels:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.8
            thickness = 2
            color = (0, 0, 0)

            # Label 1
            text_size1 = cv2.getTextSize(labels[0], font, font_scale, thickness)[0]
            text_x1 = (w1 - text_size1[0]) // 2
            cv2.putText(combined, labels[0], (text_x1, 30),
                       font, font_scale, color, thickness)

            # Label 2
            text_size2 = cv2.getTextSize(labels[1], font, font_scale, thickness)[0]
            text_x2 = w1 + gap + (w2 - text_size2[0]) // 2
            cv2.putText(combined, labels[1], (text_x2, 30),
                       font, font_scale, color, thickness)

        return combined

    @staticmethod
    def add_watermark(image: np.ndarray, text: str = "FaceAge Analyzer") -> np.ndarray:
        """
        Add watermark to image.

        Args:
            image: Input image
            text: Watermark text

        Returns:
            Watermarked image
        """
        watermarked = image.copy()

        # Add semi-transparent text in bottom-right corner
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        color = (200, 200, 200)

        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        h, w = image.shape[:2]

        x = w - text_size[0] - 10
        y = h - 10

        cv2.putText(watermarked, text, (x, y),
                   font, font_scale, color, thickness)

        return watermarked
