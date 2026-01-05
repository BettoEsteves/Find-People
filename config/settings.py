"""Settings loader for FaceAge Identity Analyzer."""
import os
from pathlib import Path
from typing import Dict, Any
import yaml


class Settings:
    """Configuration settings manager."""

    def __init__(self, config_path: str = None):
        """
        Initialize settings from YAML configuration file.

        Args:
            config_path: Path to config.yaml file. If None, uses default location.
        """
        if config_path is None:
            # Default to config/config.yaml relative to project root
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config" / "config.yaml"

        self.config_path = Path(config_path)
        self._config = self._load_config()
        self._create_directories()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        return config

    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        project_root = Path(__file__).parent.parent

        for path_key, path_value in self._config.get('paths', {}).items():
            full_path = project_root / path_value
            full_path.mkdir(parents=True, exist_ok=True)

    def get(self, key_path: str, default=None):
        """
        Get configuration value using dot notation.

        Args:
            key_path: Configuration key path (e.g., 'models.face_detection.backend')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self._config

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default

        return value

    def get_path(self, path_key: str) -> Path:
        """
        Get full path for a configured directory.

        Args:
            path_key: Path key from config (e.g., 'uploads', 'models')

        Returns:
            Absolute Path object
        """
        project_root = Path(__file__).parent.parent
        relative_path = self.get(f'paths.{path_key}')

        if relative_path is None:
            raise KeyError(f"Path key '{path_key}' not found in configuration")

        return project_root / relative_path

    @property
    def app_name(self) -> str:
        """Get application name."""
        return self.get('app.name', 'FaceAge Identity Analyzer')

    @property
    def app_version(self) -> str:
        """Get application version."""
        return self.get('app.version', '1.0.0')

    @property
    def debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        return self.get('app.debug', False)

    @property
    def enable_gpu(self) -> bool:
        """Check if GPU processing is enabled."""
        return self.get('processing.enable_gpu', True)

    @property
    def disclaimer_text(self) -> str:
        """Get ethics disclaimer text."""
        return self.get('ethics.disclaimer_text', '')


# Global settings instance
settings = Settings()
