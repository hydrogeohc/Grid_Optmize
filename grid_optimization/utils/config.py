"""
Configuration Management Utilities

Centralized configuration loading and validation for the grid optimization system.
"""

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class DatabaseConfig(BaseModel):
    """Database configuration model."""

    type: str = "sqlite"
    path: str = "gridopt.db"
    echo: bool = False
    host: Optional[str] = None
    port: Optional[int] = None
    name: Optional[str] = None


class APIConfig(BaseModel):
    """API server configuration model."""

    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False
    reload: bool = False
    cors_origins: list = ["*"]


class GridConfig(BaseModel):
    """Grid optimization configuration model."""

    default_region: str = "us-west"
    max_iterations: int = 100
    tolerance: float = 1e-6
    algorithm: str = "scipy-minimize"


class AppConfig(BaseModel):
    """Main application configuration model."""

    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    grid: GridConfig = Field(default_factory=GridConfig)
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"


def load_config(config_path: Optional[str] = None) -> AppConfig:
    """
    Load configuration from YAML file with environment-specific overrides.

    Args:
        config_path: Path to configuration file. Defaults to configs/app.yml

    Returns:
        Validated application configuration
    """
    if config_path is None:
        # Default to configs/app.yml relative to project root
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "configs" / "app.yml"

    config_data = {}

    if Path(config_path).exists():
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f) or {}

    # Environment-specific overrides
    env = os.getenv("GRID_OPTIMIZATION_ENV", "development")
    if env in config_data:
        # Merge environment-specific config
        base_config = {
            k: v
            for k, v in config_data.items()
            if k not in ["development", "staging", "production"]
        }
        env_config = config_data.get(env, {})

        # Deep merge
        for key, value in env_config.items():
            if (
                key in base_config
                and isinstance(base_config[key], dict)
                and isinstance(value, dict)
            ):
                base_config[key].update(value)
            else:
                base_config[key] = value

        config_data = base_config

    # Set default environment if not specified
    if "environment" not in config_data:
        config_data["environment"] = "development"

    return AppConfig(**config_data)


def get_database_url(config: AppConfig) -> str:
    """
    Generate database URL from configuration.

    Args:
        config: Application configuration

    Returns:
        Database connection URL
    """
    db_config = config.database

    if db_config.type == "sqlite":
        return f"sqlite:///{db_config.path}"
    elif db_config.type == "postgresql":
        return f"postgresql://{db_config.host}:{db_config.port}/{db_config.name}"
    else:
        raise ValueError(f"Unsupported database type: {db_config.type}")


# Global configuration instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get global configuration instance (singleton pattern)."""
    global _config
    if _config is None:
        _config = load_config()
    return _config
