"""
Grid Optimization System
AI-Powered Power Grid Management with NVIDIA NeMo Agent Toolkit
"""

__version__ = "1.0.0"
__author__ = "Grid Optimization Team"

# Import key components for external use
try:
    from .src.grid_core import optimize_grid, get_engine, get_session, GridState, OptimizationResult
    
    __all__ = [
        "optimize_grid",
        "get_engine", 
        "get_session",
        "GridState",
        "OptimizationResult",
    ]
except ImportError:
    # Graceful fallback if imports fail
    __all__ = []