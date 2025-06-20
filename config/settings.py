import yaml
from pathlib import Path
from typing import Dict, Any
import os

class Config:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent / "site_config.yaml"
        
        self.config_path = Path(config_path)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                config_data = yaml.safe_load(f)
                print(f"Loaded config from {self.config_path}")
                return config_data
        except FileNotFoundError:
            print(f"Config file not found at {self.config_path}, using defaults")
            return self._get_default_config()
        except Exception as e:
            print(f"Error loading config: {e}, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "llm_provider": "gpt-4o",
            "llm_temperature": 0.1,
            "browser": {
                "headless": False,
                "viewport_width": 1280,
                "viewport_height": 720,
                "timeout": 30000
            },
            "amazon": {
                "base_url": "https://amazon.com"
            },
            "task": {
                "default_threshold": 100.0,
                "currency": "USD"
            },
            "browser_use": {
                "llm_provider": "gpt-4o",
                "temperature": 0.1,
                "max_actions": 20,
                "safety_mode": True
            }
        }
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    @property
    def browser_config(self) -> Dict[str, Any]:
        return self.get("browser", {})
    
    @property
    def amazon_config(self) -> Dict[str, Any]:
        return self.get("amazon", {})
    
    @property
    def task_config(self) -> Dict[str, Any]:
        return self.get("task", {})
    
    @property
    def browser_use_config(self) -> Dict[str, Any]:
        return self.get("browser_use", {})

# Global config instance
config = Config()

# Debug print to see what config actually contains
print(f"Config type: {type(config._config)}")
print(f"Config keys: {list(config._config.keys()) if isinstance(config._config, dict) else 'Not a dict'}")