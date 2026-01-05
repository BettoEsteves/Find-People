"""Face embeddings extraction using InsightFace or FaceNet."""
import cv2
import numpy as np
from typing import Optional, Union
from loguru import logger

try:
    import insightface
    from insightface.app import FaceAnalysis
    INSIGHTFACE_AVAILABLE = True
except ImportError:
    INSIGHTFACE_AVAILABLE = False
    logger.warning("InsightFace not available")

try:
    from facenet_pytorch import InceptionResnetV1
    import torch
    FACENET_AVAILABLE = True
except ImportError:
    FACENET_AVAILABLE = False
    logger.warning("FaceNet not available")


class FaceEmbeddings:
    """
    Face embeddings extraction for facial recognition.

    This class converts face images into numerical feature vectors (embeddings)
    that can be used for similarity comparison.
    """

    def __init__(
        self,
        backend: str = "insightface",
        model_name: str = "buffalo_l",
        device: str = "cpu"
    ):
        """
        Initialize face embeddings extractor.

        Args:
            backend: Backend to use ('insightface' or 'facenet')
            model_name: Model name (for InsightFace: 'buffalo_l', 'buffalo_s', etc.)
            device: Device to use ('cpu' or 'cuda')
        """
        self.backend = backend
        self.model_name = model_name
        self.device = device
        self.model = None

        if backend == "insightface" and INSIGHTFACE_AVAILABLE:
            self._init_insightface()
        elif backend == "facenet" and FACENET_AVAILABLE:
            self._init_facenet()
        else:
            raise RuntimeError(
                f"Backend '{backend}' not available. "
                f"InsightFace available: {INSIGHTFACE_AVAILABLE}, "
                f"FaceNet available: {FACENET_AVAILABLE}"
            )

        logger.info(f"FaceEmbeddings initialized with backend: {backend}")

    def _init_insightface(self):
        """Initialize InsightFace model."""
        try:
            self.model = FaceAnalysis(
                name=self.model_name,
                providers=['CPUExecutionProvider'] if self.device == 'cpu' else ['CUDAExecutionProvider']
            )
            self.model.prepare(ctx_id=0 if self.device == 'cuda' else -1, det_size=(640, 640))
            logger.info(f"InsightFace model '{self.model_name}' loaded successfully")
        except Exception as e:
            logger.error(f"Failed to initialize InsightFace: {e}")
            raise

    def _init_facenet(self):
        """Initialize FaceNet model."""
        try:
            self.model = InceptionResnetV1(pretrained='vggface2').eval()

            if self.device == 'cuda' and torch.cuda.is_available():
                self.model = self.model.cuda()

            logger.info("FaceNet model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to initialize FaceNet: {e}")
            raise

    def extract(self, face_image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract face embedding from image.

        Args:
            face_image: Face image (BGR or RGB format)

        Returns:
            Embedding vector (numpy array) or None if extraction fails
        """
        if self.backend == "insightface":
            return self._extract_insightface(face_image)
        elif self.backend == "facenet":
            return self._extract_facenet(face_image)
        else:
            raise ValueError(f"Unknown backend: {self.backend}")

    def _extract_insightface(self, face_image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract embedding using InsightFace.

        Args:
            face_image: Face image (BGR format expected)

        Returns:
            Embedding vector or None
        """
        try:
            # InsightFace expects BGR format
            if len(face_image.shape) == 2:
                face_image = cv2.cvtColor(face_image, cv2.COLOR_GRAY2BGR)

            # Detect and extract
            faces = self.model.get(face_image)

            if not faces:
                logger.warning("No face detected in image for embedding extraction")
                return None

            # Get embedding from first (largest) face
            embedding = faces[0].embedding

            # Normalize embedding
            embedding = embedding / np.linalg.norm(embedding)

            logger.debug(f"Extracted embedding with shape: {embedding.shape}")
            return embedding

        except Exception as e:
            logger.error(f"InsightFace embedding extraction failed: {e}")
            return None

    def _extract_facenet(self, face_image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract embedding using FaceNet.

        Args:
            face_image: Face image (RGB format expected)

        Returns:
            Embedding vector or None
        """
        try:
            # Convert BGR to RGB if needed
            if len(face_image.shape) == 3 and face_image.shape[2] == 3:
                face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)

            # Resize to expected input size
            face_resized = cv2.resize(face_image, (160, 160))

            # Convert to tensor
            face_tensor = torch.from_numpy(face_resized).permute(2, 0, 1).float()
            face_tensor = (face_tensor - 127.5) / 128.0  # Normalize
            face_tensor = face_tensor.unsqueeze(0)

            if self.device == 'cuda' and torch.cuda.is_available():
                face_tensor = face_tensor.cuda()

            # Extract embedding
            with torch.no_grad():
                embedding = self.model(face_tensor)

            # Convert to numpy
            embedding = embedding.cpu().numpy().flatten()

            # Normalize
            embedding = embedding / np.linalg.norm(embedding)

            logger.debug(f"Extracted embedding with shape: {embedding.shape}")
            return embedding

        except Exception as e:
            logger.error(f"FaceNet embedding extraction failed: {e}")
            return None

    def extract_from_aligned(
        self,
        aligned_face: np.ndarray,
        skip_detection: bool = True
    ) -> Optional[np.ndarray]:
        """
        Extract embedding from pre-aligned face.

        Args:
            aligned_face: Pre-aligned face image
            skip_detection: If True, skip face detection step (faster)

        Returns:
            Embedding vector or None
        """
        if skip_detection and self.backend == "facenet":
            # For FaceNet, we can directly process aligned faces
            return self._extract_facenet(aligned_face)
        else:
            # For InsightFace or if detection is needed
            return self.extract(aligned_face)

    def batch_extract(self, face_images: list) -> list:
        """
        Extract embeddings from multiple face images.

        Args:
            face_images: List of face images

        Returns:
            List of embedding vectors (None for failed extractions)
        """
        embeddings = []

        for i, face_image in enumerate(face_images):
            logger.debug(f"Extracting embedding {i+1}/{len(face_images)}")
            embedding = self.extract(face_image)
            embeddings.append(embedding)

        return embeddings

    @property
    def embedding_size(self) -> int:
        """Get the size of embedding vectors."""
        if self.backend == "insightface":
            return 512  # Default for most InsightFace models
        elif self.backend == "facenet":
            return 512  # FaceNet embedding size
        else:
            return 0

    def is_valid_embedding(self, embedding: Optional[np.ndarray]) -> bool:
        """
        Check if embedding is valid.

        Args:
            embedding: Embedding vector to check

        Returns:
            True if valid, False otherwise
        """
        if embedding is None:
            return False

        if not isinstance(embedding, np.ndarray):
            return False

        if embedding.shape[0] != self.embedding_size:
            return False

        # Check for NaN or Inf
        if np.any(np.isnan(embedding)) or np.any(np.isinf(embedding)):
            return False

        return True
