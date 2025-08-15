"""
Grid Optimization API Routes

RESTful API endpoints for grid optimization operations.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException

from ...core.models import (
    AVAILABLE_REGIONS,
    REGION_NAMES,
    GridOptimizationRequest,
    GridOptimizationResult,
    GridStatusResponse,
    OptimizationHistory,
    RegionInfo,
)
from ...core.operations import get_latest_optimization, optimize_grid
from ...utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/grid", tags=["Grid Optimization"])


@router.get("/regions", response_model=List[RegionInfo])
async def get_available_regions():
    """Get list of available grid regions."""
    logger.info("Fetching available regions")
    return AVAILABLE_REGIONS


@router.post("/optimize", response_model=GridOptimizationResult)
async def optimize_grid_region(request: GridOptimizationRequest):
    """
    Optimize power grid for a specific region.

    Args:
        request: Grid optimization request with region and optional parameters

    Returns:
        Optimization results including supply, demand, losses, and efficiency
    """
    logger.info(f"Optimizing grid for region: {request.region}")

    if request.region not in REGION_NAMES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid region '{request.region}'. Available regions: {REGION_NAMES}",
        )

    try:
        # Run optimization
        start_time = datetime.now()
        result = optimize_grid(request.region)
        end_time = datetime.now()

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        # Add timing information
        result["optimization_time"] = (end_time - start_time).total_seconds()
        result["timestamp"] = end_time
        result["status"] = "success"

        logger.info(f"Grid optimization completed for {request.region}")
        return GridOptimizationResult(**result)

    except Exception as e:
        logger.error(f"Grid optimization failed for {request.region}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize/async", response_model=dict)
async def optimize_grid_async(request: GridOptimizationRequest, background_tasks: BackgroundTasks):
    """
    Start asynchronous grid optimization for a specific region.

    Args:
        request: Grid optimization request
        background_tasks: FastAPI background tasks

    Returns:
        Task ID for tracking optimization progress
    """
    import uuid

    if request.region not in REGION_NAMES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid region '{request.region}'. Available regions: {REGION_NAMES}",
        )

    task_id = str(uuid.uuid4())

    def run_optimization():
        logger.info(f"Background optimization started for {request.region} (Task: {task_id})")
        try:
            optimize_grid(request.region)
            logger.info(f"Background optimization completed for {request.region}")
        except Exception as e:
            logger.error(f"Background optimization failed for {request.region}: {e}")

    background_tasks.add_task(run_optimization)

    return {
        "task_id": task_id,
        "region": request.region,
        "status": "started",
        "message": "Optimization started in background",
    }


@router.get("/status/{region}", response_model=GridStatusResponse)
async def get_grid_status(region: str):
    """
    Get current grid status and optimization history for a region.

    Args:
        region: Grid region name

    Returns:
        Grid status information including current state and history
    """
    logger.info(f"Fetching grid status for region: {region}")

    if region not in REGION_NAMES:
        raise HTTPException(
            status_code=400, detail=f"Invalid region '{region}'. Available regions: {REGION_NAMES}"
        )

    try:
        result = get_latest_optimization(region)

        if "error" in result:
            # Return default status if no optimization history exists
            return GridStatusResponse(
                region=region,
                current_status="No data",
                current_load=None,
                total_capacity=None,
                efficiency=None,
                active_alerts=0,
                last_optimization="Never",
                next_scheduled="Not scheduled",
            )

        # Convert optimization result to status response
        efficiency = None
        if result.get("optimized_supply", 0) > 0:
            efficiency = f"{(1 - result.get('losses', 0) / result['optimized_supply']) * 100:.1f}%"

        return GridStatusResponse(
            region=region,
            current_status="Operational",
            current_load=result.get("optimized_demand"),
            total_capacity=result.get("optimized_supply", 0) * 1.2,  # Estimate capacity
            efficiency=efficiency,
            active_alerts=0,
            last_optimization=result.get("timestamp", "Unknown"),
            next_scheduled="Not scheduled",
        )

    except Exception as e:
        logger.error(f"Failed to get grid status for {region}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{region}", response_model=List[OptimizationHistory])
async def get_optimization_history(region: str, limit: int = 10):
    """
    Get optimization history for a region.

    Args:
        region: Grid region name
        limit: Maximum number of history entries to return

    Returns:
        List of historical optimization results
    """
    logger.info(f"Fetching optimization history for region: {region}, limit: {limit}")

    if region not in REGION_NAMES:
        raise HTTPException(
            status_code=400, detail=f"Invalid region '{region}'. Available regions: {REGION_NAMES}"
        )

    try:
        # For now, return mock history based on latest optimization
        # In a real implementation, this would query the database
        result = get_latest_optimization(region)

        if "error" in result:
            return []

        # Create a mock history entry
        history_entry = OptimizationHistory(
            id=1,
            region=region,
            timestamp=datetime.now(),
            supply=result.get("optimized_supply", 0),
            demand=result.get("optimized_demand", 0),
            losses=result.get("losses", 0),
            efficiency=(
                (1 - result.get("losses", 0) / result.get("optimized_supply", 1)) * 100
                if result.get("optimized_supply", 0) > 0
                else None
            ),
            cost_savings=result.get("cost_savings"),
        )

        return [history_entry]

    except Exception as e:
        logger.error(f"Failed to get optimization history for {region}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
