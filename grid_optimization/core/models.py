"""
Data Models

Pydantic models for API requests, responses, and data validation.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class GridOptimizationRequest(BaseModel):
    """Request model for grid optimization."""

    region: str = Field(..., description="Grid region to optimize")
    parameters: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional optimization parameters"
    )


class GridOptimizationResult(BaseModel):
    """Response model for grid optimization results."""

    region: str = Field(..., description="Grid region")
    status: str = Field(..., description="Optimization status")
    optimized_supply: float = Field(..., description="Optimized power supply in MW")
    optimized_demand: float = Field(..., description="Optimized power demand in MW")
    losses: float = Field(..., description="Power losses in MW²")
    efficiency: Optional[float] = Field(None, description="Grid efficiency percentage")
    cost_savings: Optional[float] = Field(None, description="Estimated annual cost savings")
    timestamp: Optional[datetime] = Field(None, description="Optimization timestamp")
    optimization_time: Optional[float] = Field(
        None, description="Time taken for optimization in seconds"
    )


class GridStatusResponse(BaseModel):
    """Response model for grid status information."""

    region: str = Field(..., description="Grid region")
    current_status: str = Field(..., description="Current grid status")
    current_load: Optional[float] = Field(None, description="Current load in MW")
    total_capacity: Optional[float] = Field(None, description="Total capacity in MW")
    efficiency: Optional[str] = Field(None, description="Current efficiency percentage")
    active_alerts: int = Field(0, description="Number of active alerts")
    last_optimization: str = Field("Never", description="Last optimization timestamp")
    next_scheduled: str = Field("Not scheduled", description="Next scheduled optimization")


class RegionInfo(BaseModel):
    """Model for region information."""

    name: str = Field(..., description="Region name")
    display_name: str = Field(..., description="Human-readable region name")
    description: Optional[str] = Field(None, description="Region description")
    capacity: Optional[float] = Field(None, description="Total capacity in MW")
    status: str = Field("active", description="Region status")


class OptimizationHistory(BaseModel):
    """Model for optimization history entry."""

    id: int = Field(..., description="History entry ID")
    region: str = Field(..., description="Grid region")
    timestamp: datetime = Field(..., description="Optimization timestamp")
    supply: float = Field(..., description="Optimized supply in MW")
    demand: float = Field(..., description="Optimized demand in MW")
    losses: float = Field(..., description="Power losses in MW²")
    efficiency: Optional[float] = Field(None, description="Grid efficiency")
    cost_savings: Optional[float] = Field(None, description="Cost savings")


class HealthCheckResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")
    database_connected: bool = Field(..., description="Database connection status")
    components: Dict[str, str] = Field(default_factory=dict, description="Component status")


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")


# Constants
AVAILABLE_REGIONS = [
    RegionInfo(name="us-west", display_name="US West", description="Western United States grid"),
    RegionInfo(name="us-east", display_name="US East", description="Eastern United States grid"),
    RegionInfo(
        name="us-central", display_name="US Central", description="Central United States grid"
    ),
    RegionInfo(name="pgae", display_name="PG&E", description="Pacific Gas & Electric grid"),
]

REGION_NAMES = [region.name for region in AVAILABLE_REGIONS]
