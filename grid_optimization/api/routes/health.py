"""
Health Check API Routes

System health and monitoring endpoints.
"""

import sys
from datetime import datetime

from fastapi import APIRouter, HTTPException

from ...core.database import get_engine
from ...core.models import HealthCheckResponse
from ...utils.config import get_config
from ...utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Comprehensive health check endpoint.

    Returns:
        System health status including database connectivity and component status
    """
    logger.debug("Performing health check")

    components = {}
    database_connected = False
    overall_status = "healthy"

    # Check database connectivity
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute("SELECT 1").fetchone()
        database_connected = True
        components["database"] = "healthy"
        logger.debug("Database connection: OK")
    except Exception as e:
        database_connected = False
        components["database"] = f"unhealthy: {str(e)}"
        overall_status = "degraded"
        logger.warning(f"Database connection failed: {e}")

    # Check Python environment
    components["python_version"] = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    components["platform"] = sys.platform

    # Check core modules
    try:
        from ...core.operations import optimize_grid
        optimize_grid  # Mark as used for linting

        components["grid_optimization"] = "available"
    except Exception as e:
        components["grid_optimization"] = f"unavailable: {str(e)}"
        overall_status = "unhealthy"

    # Check NAT integration
    try:
        from ...integrations.nat.register import optimize_grid_region
        optimize_grid_region  # Mark as used for linting

        components["nat_integration"] = "available"
    except Exception as e:
        components["nat_integration"] = f"unavailable: {str(e)}"
        # NAT is optional, don't mark overall status as unhealthy

    # Check configuration
    try:
        config = get_config()
        components["configuration"] = f"loaded ({config.environment})"
    except Exception as e:
        components["configuration"] = f"failed: {str(e)}"
        overall_status = "degraded"

    return HealthCheckResponse(
        status=overall_status,
        version="1.0.0",  # Should be loaded from package metadata
        timestamp=datetime.now(),
        database_connected=database_connected,
        components=components,
    )


@router.get("/ready")
async def readiness_check():
    """
    Kubernetes-style readiness check.

    Returns:
        Simple ready/not ready status
    """
    try:
        # Check if core services are available
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute("SELECT 1").fetchone()

        from ...core.operations import optimize_grid
        optimize_grid  # Mark as used for linting

        return {"status": "ready"}

    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready")


@router.get("/live")
async def liveness_check():
    """
    Kubernetes-style liveness check.

    Returns:
        Simple alive status
    """
    return {"status": "alive", "timestamp": datetime.now().isoformat()}
