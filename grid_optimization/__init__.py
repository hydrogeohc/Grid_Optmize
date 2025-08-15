"""
Grid Optimization System

A comprehensive AI-powered grid optimization platform with NVIDIA NeMo Agent Toolkit integration.
"""

__version__ = "1.0.0"
__author__ = "Grid Optimization Team"

from .core.database import get_engine, get_session
from .core.operations import get_latest_optimization, optimize_grid

__all__ = ["optimize_grid", "get_latest_optimization", "get_engine", "get_session"]
