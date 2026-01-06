"""Face aging module for simulating age progression."""
import cv2
import numpy as np
from typing import Optional, Tuple
from loguru import logger
from PIL import Image, ImageEnhance, ImageFilter


class FaceAging:
    """
    Face aging simulation using image processing techniques.

    This implementation uses a combination of:
    - Texture and wrinkle enhancement
    - Skin tone adjustment
    - Feature morphing
    - Style transfer techniques

    Note: This is a simplified implementation. For production use,
    consider using deep learning models like SAM, IPCGAN, or StyleGAN-based approaches.
    """

    def __init__(self, method: str = "style_transfer"):
        """
        Initialize face aging module.

        Args:
            method: Aging method ('style_transfer', 'interpolation')
        """
        self.method = method
        logger.info(f"FaceAging initialized with method: {method}")

    def age_progression(
        self,
        face_image: np.ndarray,
        current_age: int,
        target_age: int
    ) -> np.ndarray:
        """
        Simulate age progression from current age to target age.

        Args:
            face_image: Input face image (RGB or BGR)
            current_age: Current age of person in image
            target_age: Target age to simulate

        Returns:
            Aged face image

        Raises:
            ValueError: If age parameters are invalid
        """
        if current_age < 0 or target_age < 0:
            raise ValueError("Ages must be non-negative")

        if target_age <= current_age:
            logger.warning("Target age is not greater than current age")
            return face_image.copy()

        age_delta = target_age - current_age
        logger.info(f"Simulating age progression: {current_age} -> {target_age} (delta: {age_delta} years)")

        if self.method == "style_transfer":
            return self._age_style_transfer(face_image, age_delta, current_age, target_age)
        elif self.method == "interpolation":
            return self._age_interpolation(face_image, age_delta)
        else:
            raise ValueError(f"Unknown aging method: {self.method}")

    def _age_style_transfer(
        self,
        image: np.ndarray,
        age_delta: int,
        current_age: int,
        target_age: int
    ) -> np.ndarray:
        """
        Apply aging effects using style transfer approach.

        This method applies multiple transformations:
        1. Skin texture changes (wrinkles, fine lines)
        2. Color/tone adjustments
        3. Contrast and sharpness changes
        4. Feature sagging simulation

        Args:
            image: Input face image
            age_delta: Years to age
            current_age: Current age
            target_age: Target age

        Returns:
            Aged face image
        """
        # Convert to PIL for better image manipulation
        if len(image.shape) == 3 and image.shape[2] == 3:
            # Assume BGR from OpenCV
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        else:
            pil_image = Image.fromarray(image)

        # Calculate aging intensity (0.0 to 1.0)
        # More aggressive aging for larger age gaps
        intensity = min(age_delta / 60.0, 1.0)

        # Apply aging transformations
        aged_image = pil_image.copy()

        # 1. Skin tone adjustment (yellowing/darkening with age)
        aged_image = self._adjust_skin_tone(aged_image, intensity, target_age)

        # 2. Add wrinkles and texture
        aged_image = self._add_wrinkles(aged_image, intensity)

        # 3. Reduce skin smoothness
        aged_image = self._reduce_smoothness(aged_image, intensity)

        # 4. Adjust contrast (skin loses elasticity)
        aged_image = self._adjust_contrast(aged_image, intensity)

        # 5. Simulate feature sagging (especially for large age jumps)
        if age_delta > 20:
            aged_image = self._simulate_sagging(aged_image, intensity)

        # 6. Add age spots (for older ages)
        if target_age > 50:
            aged_image = self._add_age_spots(aged_image, intensity)

        # Convert back to numpy array
        result = np.array(aged_image)

        # Convert back to BGR if original was BGR
        if len(image.shape) == 3 and image.shape[2] == 3:
            result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)

        return result

    def _adjust_skin_tone(self, image: Image.Image, intensity: float, target_age: int) -> Image.Image:
        """Adjust skin tone to simulate aging."""
        # Older skin tends to be yellower and darker - mais agressivo
        enhancer = ImageEnhance.Color(image)
        # Reduce saturation
        image = enhancer.enhance(1.0 - intensity * 0.35)

        # Adjust brightness (darkening)
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.0 - intensity * 0.20)

        return image

    def _add_wrinkles(self, image: Image.Image, intensity: float) -> Image.Image:
        """Add wrinkle texture to simulate aging."""
        # Create detail map using edge detection
        gray = image.convert('L')

        # Apply edge enhancement to create wrinkle effect
        edges = gray.filter(ImageFilter.FIND_EDGES)

        # Enhance edges - mais agressivo
        enhancer = ImageEnhance.Contrast(edges)
        edges = enhancer.enhance(3.5)

        # Blend edges back with original
        edges_rgb = edges.convert('RGB')

        # Blend with opacity based on intensity - mais agressivo
        alpha = intensity * 0.40

        # Convert to numpy for blending
        img_arr = np.array(image).astype(np.float32)
        edges_arr = np.array(edges_rgb).astype(np.float32)

        # Darken along edges (wrinkles are darker) - mais agressivo
        wrinkled = img_arr - (edges_arr * alpha * 0.6)
        wrinkled = np.clip(wrinkled, 0, 255).astype(np.uint8)

        return Image.fromarray(wrinkled)

    def _reduce_smoothness(self, image: Image.Image, intensity: float) -> Image.Image:
        """Reduce skin smoothness to simulate texture changes."""
        # Add noise to simulate skin texture changes - mais agressivo
        img_arr = np.array(image).astype(np.float32)

        # Generate noise - mais agressivo
        noise = np.random.normal(0, intensity * 5.0, img_arr.shape)

        # Add noise
        textured = img_arr + noise
        textured = np.clip(textured, 0, 255).astype(np.uint8)

        # Apply slight blur to make it look natural
        result = Image.fromarray(textured)
        result = result.filter(ImageFilter.GaussianBlur(radius=0.5))

        return result

    def _adjust_contrast(self, image: Image.Image, intensity: float) -> Image.Image:
        """Adjust contrast to simulate loss of skin elasticity."""
        enhancer = ImageEnhance.Contrast(image)
        # Increase contrast - mais agressivo
        factor = 1.0 + intensity * 0.35
        return enhancer.enhance(factor)

    def _simulate_sagging(self, image: Image.Image, intensity: float) -> Image.Image:
        """Simulate facial feature sagging (simplified)."""
        img_arr = np.array(image)
        h, w = img_arr.shape[:2]

        # Apply subtle vertical stretching in lower face region
        # This simulates sagging of facial features

        # Create mesh grid
        rows, cols = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')

        # Apply slight downward displacement in lower half
        displacement = intensity * 2.0  # pixels
        mask = (rows > h * 0.5).astype(np.float32)
        rows_displaced = rows + (mask * displacement * (rows - h * 0.5) / (h * 0.5))
        rows_displaced = np.clip(rows_displaced, 0, h - 1).astype(np.float32)

        # Remap image
        sagged = cv2.remap(
            img_arr,
            cols.astype(np.float32),
            rows_displaced,
            cv2.INTER_LINEAR
        )

        return Image.fromarray(sagged)

    def _add_age_spots(self, image: Image.Image, intensity: float) -> Image.Image:
        """Add age spots for older ages."""
        img_arr = np.array(image).astype(np.float32)
        h, w = img_arr.shape[:2]

        # Generate age spots - mais agressivo
        num_spots = int(intensity * 40)

        for _ in range(num_spots):
            # Random position
            x = np.random.randint(w // 4, 3 * w // 4)
            y = np.random.randint(h // 4, 3 * h // 4)

            # Random size - maior
            radius = np.random.randint(2, 5)

            # Random darkness - mais escuro
            darkness = np.random.uniform(0.65, 0.85)

            # Draw circular spot
            cv2.circle(img_arr, (x, y), radius,
                      (img_arr[y, x] * darkness).tolist(), -1)

        result = np.clip(img_arr, 0, 255).astype(np.uint8)
        return Image.fromarray(result)

    def _age_interpolation(self, image: np.ndarray, age_delta: int) -> np.ndarray:
        """
        Simpler aging method using interpolation (fallback).

        Args:
            image: Input face image
            age_delta: Years to age

        Returns:
            Aged face image
        """
        # Simple approach: just apply basic transformations
        intensity = min(age_delta / 60.0, 1.0)

        # Convert to PIL
        if len(image.shape) == 3:
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        else:
            pil_image = Image.fromarray(image)

        # Apply basic aging
        aged = self._adjust_skin_tone(pil_image, intensity, 0)
        aged = self._reduce_smoothness(aged, intensity)

        # Convert back
        result = np.array(aged)
        if len(image.shape) == 3:
            result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)

        return result

    def get_confidence_score(self, age_delta: int) -> float:
        """
        Get confidence score for aging simulation.

        Larger age deltas typically have lower confidence.

        Args:
            age_delta: Age difference in years

        Returns:
            Confidence score (0.0 to 1.0)
        """
        if age_delta <= 0:
            return 1.0
        elif age_delta <= 10:
            return 0.85
        elif age_delta <= 20:
            return 0.70
        elif age_delta <= 40:
            return 0.55
        else:
            return 0.40
