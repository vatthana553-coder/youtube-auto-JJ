"""
Utility module for configuration management.
Handles loading and validating configuration from YAML files.
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for the video generation pipeline."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize configuration from YAML file.
        
        Args:
            config_path: Path to the configuration YAML file
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            logger.warning(f"Config file {self.config_path} not found. Using defaults.")
            self.config = self._get_default_config()
            return
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self.config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration values."""
        return {
            'general': {
                'project_name': 'my_viral_short',
                'duration': 45,
                'resolution': '1080x1920',
                'fps': 30,
                'output_format': 'mp4',
                'verbose': True
            },
            'niche': {
                'default': 'science',
                'available': ['facts', 'history', 'science', 'mysteries', 'finance', 'what_if'],
                'tone': 'curious'
            },
            'tts': {
                'engine': 'edge-tts',
                'voice': 'en-US-JennyNeural',
                'speed': 1.0,
                'pitch': 0,
                'volume': 100
            },
            'visuals': {
                'style': 'mixed',
                'motion_effects': True,
                'ken_burns': True,
                'transition_duration': 0.5,
                'zoom_intensity': 0.1,
                'fallback_to_color': True
            },
            'llm': {
                'provider': 'mock',
                'model': 'llama2',
                'max_tokens': 500,
                'temperature': 0.7,
                'timeout': 30
            },
            'subtitles': {
                'enabled': True,
                'style': 'modern',
                'font': 'Arial',
                'font_size': 48,
                'font_color': '#FFFFFF',
                'stroke_color': '#000000',
                'stroke_width': 2,
                'position': 'bottom',
                'highlight_keywords': True
            },
            'audio': {
                'background_music_volume': 0.15,
                'sfx_volume': 0.8,
                'music_fade_in': 1.0,
                'music_fade_out': 2.0,
                'normalize_audio': True,
                'target_loudness': -16
            },
            'paths': {
                'projects_root': 'projects',
                'assets_root': 'assets',
                'templates_root': 'templates'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'tts.voice')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'tts.voice')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save_config(self, path: Optional[str] = None) -> None:
        """
        Save current configuration to YAML file.
        
        Args:
            path: Optional path to save to (defaults to original config_path)
        """
        save_path = Path(path) if path else self.config_path
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
            logger.info(f"Configuration saved to {save_path}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def validate(self) -> bool:
        """
        Validate configuration values.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        required_sections = ['general', 'niche', 'tts', 'visuals']
        
        for section in required_sections:
            if section not in self.config:
                logger.error(f"Missing required configuration section: {section}")
                return False
        
        # Validate duration
        duration = self.get('general.duration', 45)
        if not (10 <= duration <= 180):
            logger.error(f"Invalid duration: {duration}. Must be between 10 and 180 seconds.")
            return False
        
        # Validate resolution
        resolution = self.get('general.resolution', '1080x1920')
        if 'x' not in resolution:
            logger.error(f"Invalid resolution format: {resolution}")
            return False
        
        return True
    
    def get_project_paths(self, project_name: str) -> Dict[str, Path]:
        """
        Get all paths for a specific project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Dictionary of path names to Path objects
        """
        base_path = Path(self.get('paths.projects_root', 'projects')) / project_name
        
        return {
            'base': base_path,
            'script': base_path / 'script',
            'audio': base_path / 'audio',
            'visuals': base_path / 'visuals',
            'subtitles': base_path / 'subtitles',
            'output': base_path / 'output',
            'metadata': base_path / 'metadata'
        }
    
    def ensure_project_dirs(self, project_name: str) -> Dict[str, Path]:
        """
        Create project directories if they don't exist.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Dictionary of path names to Path objects
        """
        paths = self.get_project_paths(project_name)
        
        for path_name, path_obj in paths.items():
            path_obj.mkdir(parents=True, exist_ok=True)
        
        return paths


# Global config instance
_config_instance: Optional[Config] = None


def get_config(config_path: str = "config.yaml") -> Config:
    """
    Get or create global configuration instance.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance


def reload_config(config_path: str = "config.yaml") -> Config:
    """
    Reload configuration from file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Config instance
    """
    global _config_instance
    _config_instance = Config(config_path)
    return _config_instance
