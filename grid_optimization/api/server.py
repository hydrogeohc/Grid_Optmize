"""
Grid Optimization API Server

FastAPI-based REST API for the grid optimization system.
"""

from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ..utils.config import get_config
from ..utils.logging import get_logger, setup_logging
from .routes import grid, health

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup/shutdown."""

    # Startup
    logger.info("🚀 Starting Grid Optimization API Server...")
    try:
        # Load configuration
        config = get_config()
        logger.info(f"📋 Configuration loaded - Environment: {config.environment}")

        # Initialize database
        from ..core.database import get_engine

        get_engine()
        logger.info("🗄️  Database connection established")

        logger.info("✅ Grid Optimization API Server started successfully")
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        raise

    yield

    # Shutdown
    logger.info("🔄 Shutting down Grid Optimization API Server...")
    logger.info("✅ Server shutdown complete")


# Initialize FastAPI app
app = FastAPI(
    title="Grid Optimization API",
    description="AI-powered grid optimization system with NVIDIA NeMo Agent Toolkit integration",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Get configuration
config = get_config()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with consistent error format."""
    return {
        "error": "HTTP Error",
        "message": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.now().isoformat(),
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions with consistent error format."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "timestamp": datetime.now().isoformat(),
    }


# Include routers
app.include_router(health.router)
app.include_router(grid.router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Grid Optimization API",
        "version": "1.0.0",
        "description": "AI-powered grid optimization system",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "timestamp": datetime.now().isoformat(),
    }


# API Info endpoint
@app.get("/info")
async def api_info():
    """Get detailed API information."""
    config = get_config()
    return {
        "api": {
            "name": "Grid Optimization API",
            "version": "1.0.0",
            "environment": config.environment,
            "debug": config.debug,
        },
        "endpoints": {
            "grid_optimization": "/grid/optimize",
            "grid_status": "/grid/status/{region}",
            "available_regions": "/grid/regions",
            "optimization_history": "/grid/history/{region}",
            "health_check": "/health",
            "api_docs": "/docs",
        },
        "available_regions": ["us-west", "us-east", "us-central", "pgae"],
        "features": [
            "Real-time grid optimization",
            "Multi-region support",
            "Async optimization jobs",
            "Historical data tracking",
            "Health monitoring",
            "NAT toolkit integration",
        ],
    }


def main():
    """Main entry point for running the server."""
    config = get_config()

    logger.info(f"🌐 Starting server on {config.api.host}:{config.api.port}")

    uvicorn.run(
        "grid_optimization.api.server:app",
        host=config.api.host,
        port=config.api.port,
        reload=config.api.reload,
        log_level="info" if config.debug else "warning",
    )


if __name__ == "__main__":
    main()
