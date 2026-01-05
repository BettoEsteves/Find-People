"""Face comparison and similarity calculation module."""
import numpy as np
from typing import Tuple, Dict, Optional
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean
from loguru import logger


class FaceComparator:
    """
    Face comparison using embedding similarity metrics.

    This class compares face embeddings and provides similarity scores
    with confidence estimates.
    """

    def __init__(self, similarity_threshold: float = 0.4):
        """
        Initialize face comparator.

        Args:
            similarity_threshold: Minimum similarity for positive match (0.0-1.0)
        """
        self.similarity_threshold = similarity_threshold
        logger.info(f"FaceComparator initialized with threshold: {similarity_threshold}")

    def compare(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray,
        method: str = "cosine"
    ) -> Dict[str, float]:
        """
        Compare two face embeddings.

        Args:
            embedding1: First face embedding
            embedding2: Second face embedding
            method: Similarity method ('cosine' or 'euclidean')

        Returns:
            Dictionary containing:
                - similarity: Similarity score (0.0-1.0)
                - distance: Distance metric
                - match: Boolean indicating if faces match
                - confidence: Confidence level (0.0-1.0)
        """
        if embedding1 is None or embedding2 is None:
            logger.error("Cannot compare None embeddings")
            return {
                'similarity': 0.0,
                'distance': float('inf'),
                'match': False,
                'confidence': 0.0
            }

        # Ensure embeddings are 2D for sklearn
        emb1 = embedding1.reshape(1, -1)
        emb2 = embedding2.reshape(1, -1)

        if method == "cosine":
            similarity, distance = self._cosine_similarity(emb1, emb2)
        elif method == "euclidean":
            similarity, distance = self._euclidean_similarity(emb1, emb2)
        else:
            raise ValueError(f"Unknown similarity method: {method}")

        # Determine if it's a match
        match = similarity >= self.similarity_threshold

        # Calculate confidence
        confidence = self._calculate_confidence(similarity, distance, method)

        result = {
            'similarity': float(similarity),
            'distance': float(distance),
            'match': bool(match),
            'confidence': float(confidence)
        }

        logger.info(
            f"Comparison result: similarity={similarity:.4f}, "
            f"distance={distance:.4f}, match={match}, confidence={confidence:.4f}"
        )

        return result

    def _cosine_similarity(
        self,
        emb1: np.ndarray,
        emb2: np.ndarray
    ) -> Tuple[float, float]:
        """
        Calculate cosine similarity.

        Args:
            emb1: First embedding (2D)
            emb2: Second embedding (2D)

        Returns:
            Tuple of (similarity, distance)
        """
        similarity = cosine_similarity(emb1, emb2)[0, 0]

        # Convert to distance (1 - similarity)
        distance = 1.0 - similarity

        return similarity, distance

    def _euclidean_similarity(
        self,
        emb1: np.ndarray,
        emb2: np.ndarray
    ) -> Tuple[float, float]:
        """
        Calculate Euclidean distance and convert to similarity.

        Args:
            emb1: First embedding (2D)
            emb2: Second embedding (2D)

        Returns:
            Tuple of (similarity, distance)
        """
        distance = euclidean(emb1[0], emb2[0])

        # Convert distance to similarity (0-1 scale)
        # Using exponential decay
        similarity = np.exp(-distance / 2.0)

        return similarity, distance

    def _calculate_confidence(
        self,
        similarity: float,
        distance: float,
        method: str
    ) -> float:
        """
        Calculate confidence score for the comparison.

        Confidence is based on:
        - How far the similarity is from the threshold
        - The absolute similarity value

        Args:
            similarity: Similarity score
            distance: Distance metric
            method: Method used

        Returns:
            Confidence score (0.0-1.0)
        """
        # Base confidence on similarity
        if method == "cosine":
            # For cosine similarity, confidence increases with higher similarity
            if similarity >= self.similarity_threshold:
                # Positive match - confidence based on how much above threshold
                confidence = 0.5 + (similarity - self.similarity_threshold) / (1.0 - self.similarity_threshold) * 0.5
            else:
                # Negative match - confidence based on how much below threshold
                confidence = similarity / self.similarity_threshold * 0.5
        else:
            # For Euclidean, use similar logic
            confidence = similarity

        # Clamp to [0, 1]
        confidence = np.clip(confidence, 0.0, 1.0)

        return confidence

    def similarity_to_percentage(self, similarity: float) -> float:
        """
        Convert similarity score to percentage.

        Args:
            similarity: Similarity score (0.0-1.0)

        Returns:
            Percentage (0-100)
        """
        return similarity * 100.0

    def get_match_label(self, similarity: float) -> str:
        """
        Get human-readable match label.

        Args:
            similarity: Similarity score

        Returns:
            Match label string
        """
        if similarity >= 0.8:
            return "Very High Match"
        elif similarity >= 0.7:
            return "High Match"
        elif similarity >= 0.6:
            return "Good Match"
        elif similarity >= 0.5:
            return "Moderate Match"
        elif similarity >= 0.4:
            return "Low Match"
        else:
            return "No Match"

    def batch_compare(
        self,
        reference_embedding: np.ndarray,
        query_embeddings: list,
        method: str = "cosine"
    ) -> list:
        """
        Compare one reference embedding against multiple query embeddings.

        Args:
            reference_embedding: Reference face embedding
            query_embeddings: List of query face embeddings
            method: Similarity method

        Returns:
            List of comparison results
        """
        results = []

        for i, query_embedding in enumerate(query_embeddings):
            logger.debug(f"Comparing query {i+1}/{len(query_embeddings)}")
            result = self.compare(reference_embedding, query_embedding, method)
            results.append(result)

        return results

    def find_best_match(
        self,
        reference_embedding: np.ndarray,
        candidate_embeddings: list,
        method: str = "cosine"
    ) -> Tuple[int, Dict[str, float]]:
        """
        Find best matching face from candidates.

        Args:
            reference_embedding: Reference face embedding
            candidate_embeddings: List of candidate face embeddings
            method: Similarity method

        Returns:
            Tuple of (best_index, comparison_result)
        """
        if not candidate_embeddings:
            return -1, {
                'similarity': 0.0,
                'distance': float('inf'),
                'match': False,
                'confidence': 0.0
            }

        # Compare with all candidates
        results = self.batch_compare(reference_embedding, candidate_embeddings, method)

        # Find best match
        best_idx = max(range(len(results)), key=lambda i: results[i]['similarity'])

        return best_idx, results[best_idx]

    def create_similarity_matrix(
        self,
        embeddings: list,
        method: str = "cosine"
    ) -> np.ndarray:
        """
        Create similarity matrix for multiple embeddings.

        Args:
            embeddings: List of face embeddings
            method: Similarity method

        Returns:
            N x N similarity matrix
        """
        n = len(embeddings)
        matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(i, n):
                if i == j:
                    matrix[i, j] = 1.0
                else:
                    result = self.compare(embeddings[i], embeddings[j], method)
                    similarity = result['similarity']
                    matrix[i, j] = similarity
                    matrix[j, i] = similarity

        return matrix

    def get_confidence_level(self, confidence: float) -> str:
        """
        Get human-readable confidence level.

        Args:
            confidence: Confidence score (0.0-1.0)

        Returns:
            Confidence level string
        """
        if confidence >= 0.9:
            return "Very High"
        elif confidence >= 0.75:
            return "High"
        elif confidence >= 0.6:
            return "Moderate"
        elif confidence >= 0.4:
            return "Low"
        else:
            return "Very Low"
