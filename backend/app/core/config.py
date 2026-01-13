"""
Configuration Management
"""

import yaml
from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._load_env_overrides()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def _load_env_overrides(self):
        """Override config with environment variables"""
        # Database overrides
        if os.getenv('MONGODB_URI'):
            self.config.setdefault('database', {})['mongodb']['connection_string'] = os.getenv('MONGODB_URI')
        
        if os.getenv('POSTGRES_URI'):
            self.config.setdefault('database', {})['postgresql']['connection_string'] = os.getenv('POSTGRES_URI')
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value by key (supports dot notation)"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def __getitem__(self, key: str) -> Any:
        """Get config value using bracket notation"""
        return self.get(key)
