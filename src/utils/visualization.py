"""Visualization utilities for face analysis results."""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict
from loguru import logger


class Visualization:
    """Utilities for visualizing face analysis results."""

    @staticmethod
    def draw_bounding_box(
        image: np.ndarray,
        bbox: List[int],
        label: str = "",
        color: Tuple[int, int, int] = (0, 255, 0),
        thickness: int = 2
    ) -> np.ndarray:
        """
        Draw bounding box on image.

        Args:
            image: Input image
            bbox: Bounding box [x1, y1, x2, y2]
            label: Label text
            color: Box color (BGR)
            thickness: Line thickness

        Returns:
            Image with bounding box
        """
        vis_image = image.copy()

        x1, y1, x2, y2 = map(int, bbox)

        # Draw rectangle
        cv2.rectangle(vis_image, (x1, y1), (x2, y2), color, thickness)

        # Draw label
        if label:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            text_thickness = 2

            # Get text size
            (text_w, text_h), baseline = cv2.getTextSize(
                label, font, font_scale, text_thickness
            )

            # Draw background rectangle for text
            cv2.rectangle(
                vis_image,
                (x1, y1 - text_h - baseline - 5),
                (x1 + text_w, y1),
                color,
                -1
            )

            # Draw text
            cv2.putText(
                vis_image,
                label,
                (x1, y1 - baseline - 5),
                font,
                font_scale,
                (255, 255, 255),
                text_thickness
            )

        return vis_image

    @staticmethod
    def draw_landmarks(
        image: np.ndarray,
        landmarks: Dict[str, Tuple[float, float]],
        color: Tuple[int, int, int] = (0, 0, 255),
        radius: int = 3
    ) -> np.ndarray:
        """
        Draw facial landmarks on image.

        Args:
            image: Input image
            landmarks: Dictionary of landmark points
            color: Point color (BGR)
            radius: Point radius

        Returns:
            Image with landmarks
        """
        vis_image = image.copy()

        for name, (x, y) in landmarks.items():
            cv2.circle(vis_image, (int(x), int(y)), radius, color, -1)

        return vis_image

    @staticmethod
    def create_comparison_grid(
        original_image: np.ndarray,
        aged_image: np.ndarray,
        similarity_score: float,
        original_age: int,
        target_age: int,
        confidence: float
    ) -> np.ndarray:
        """
        Create comparison grid with images and metrics.

        Args:
            original_image: Original face image
            aged_image: Aged face image
            similarity_score: Similarity score (0-1)
            original_age: Original age
            target_age: Target age
            confidence: Confidence score

        Returns:
            Comparison grid image
        """
        # Ensure same size
        h = max(original_image.shape[0], aged_image.shape[0])
        w = max(original_image.shape[1], aged_image.shape[1])

        original_resized = cv2.resize(original_image, (w, h))
        aged_resized = cv2.resize(aged_image, (w, h))

        # Create side-by-side
        gap = 40
        grid_h = h + 120  # Extra space for text
        grid_w = w * 2 + gap

        grid = np.ones((grid_h, grid_w, 3), dtype=np.uint8) * 255

        # Place images
        grid[60:60 + h, :w] = original_resized
        grid[60:60 + h, w + gap:] = aged_resized

        # Add titles
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        thickness = 2
        color = (0, 0, 0)

        # Original image title
        title1 = f"Original (Age: {original_age})"
        text_size1 = cv2.getTextSize(title1, font, font_scale, thickness)[0]
        text_x1 = (w - text_size1[0]) // 2
        cv2.putText(grid, title1, (text_x1, 35), font, font_scale, color, thickness)

        # Aged image title
        title2 = f"Aged Simulation (Age: {target_age})"
        text_size2 = cv2.getTextSize(title2, font, font_scale, thickness)[0]
        text_x2 = w + gap + (w - text_size2[0]) // 2
        cv2.putText(grid, title2, (text_x2, 35), font, font_scale, color, thickness)

        # Add metrics at bottom
        metrics_y = h + 90

        # Similarity score
        similarity_text = f"Similarity: {similarity_score * 100:.1f}%"
        cv2.putText(grid, similarity_text, (20, metrics_y),
                   font, 0.7, (0, 100, 0), 2)

        # Confidence
        confidence_text = f"Confidence: {confidence * 100:.1f}%"
        cv2.putText(grid, confidence_text, (grid_w // 2, metrics_y),
                   font, 0.7, (0, 100, 0), 2)

        return grid

    @staticmethod
    def create_similarity_bar(
        similarity_score: float,
        width: int = 600,
        height: int = 50
    ) -> np.ndarray:
        """
        Create horizontal bar showing similarity score.

        Args:
            similarity_score: Similarity score (0-1)
            width: Bar width
            height: Bar height

        Returns:
            Bar image
        """
        bar = np.ones((height, width, 3), dtype=np.uint8) * 255

        # Draw background bar
        cv2.rectangle(bar, (10, 10), (width - 10, height - 10), (200, 200, 200), -1)

        # Calculate fill width
        fill_width = int((width - 20) * similarity_score)

        # Determine color based on score
        if similarity_score >= 0.7:
            color = (0, 200, 0)  # Green
        elif similarity_score >= 0.5:
            color = (0, 165, 255)  # Orange
        else:
            color = (0, 0, 200)  # Red

        # Draw filled portion
        if fill_width > 0:
            cv2.rectangle(bar, (10, 10), (10 + fill_width, height - 10), color, -1)

        # Add percentage text
        text = f"{similarity_score * 100:.1f}%"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2

        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2

        cv2.putText(bar, text, (text_x, text_y), font, font_scale, (0, 0, 0), thickness)

        return bar

    @staticmethod
    def create_feature_comparison(
        features1: Dict[str, float],
        features2: Dict[str, float],
        width: int = 600,
        height: int = 400
    ) -> np.ndarray:
        """
        Create bar chart comparing facial features.

        Args:
            features1: First set of features
            features2: Second set of features
            width: Chart width
            height: Chart height

        Returns:
            Chart image
        """
        # Create plot
        fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)

        feature_names = list(features1.keys())
        values1 = list(features1.values())
        values2 = list(features2.values())

        x = np.arange(len(feature_names))
        bar_width = 0.35

        # Create bars
        ax.bar(x - bar_width / 2, values1, bar_width, label='Original', color='blue', alpha=0.7)
        ax.bar(x + bar_width / 2, values2, bar_width, label='Aged', color='orange', alpha=0.7)

        # Customize plot
        ax.set_xlabel('Features')
        ax.set_ylabel('Values')
        ax.set_title('Feature Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(feature_names, rotation=45, ha='right')
        ax.legend()

        plt.tight_layout()

        # Convert plot to image
        fig.canvas.draw()
        img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        plt.close(fig)

        # Convert RGB to BGR for OpenCV
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        return img

    @staticmethod
    def add_text_overlay(
        image: np.ndarray,
        text: str,
        position: str = "top",
        background_color: Tuple[int, int, int] = (0, 0, 0),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        alpha: float = 0.7
    ) -> np.ndarray:
        """
        Add text overlay to image.

        Args:
            image: Input image
            text: Text to add
            position: Position ('top', 'bottom', 'center')
            background_color: Background color (BGR)
            text_color: Text color (BGR)
            alpha: Background transparency

        Returns:
            Image with text overlay
        """
        overlay = image.copy()
        h, w = image.shape[:2]

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        padding = 10

        # Get text size
        text_size, baseline = cv2.getTextSize(text, font, font_scale, thickness)
        text_w, text_h = text_size

        # Determine position
        if position == "top":
            rect_y1 = 0
            rect_y2 = text_h + 2 * padding
            text_y = padding + text_h
        elif position == "bottom":
            rect_y1 = h - text_h - 2 * padding
            rect_y2 = h
            text_y = h - padding
        else:  # center
            rect_y1 = (h - text_h - 2 * padding) // 2
            rect_y2 = rect_y1 + text_h + 2 * padding
            text_y = rect_y1 + padding + text_h

        # Draw background rectangle
        cv2.rectangle(overlay, (0, rect_y1), (w, rect_y2), background_color, -1)

        # Blend with original
        result = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

        # Draw text
        text_x = (w - text_w) // 2
        cv2.putText(result, text, (text_x, text_y), font, font_scale, text_color, thickness)

        return result
