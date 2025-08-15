"""
NAT Integration Module for Grid Optimization
Provides async functions compatible with NVIDIA NeMo Agent Toolkit
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json

from .operations import optimize_grid as sync_optimize_grid
from .db import get_engine, get_session, GridState, OptimizationResult
from .security import validate_region_access

logger = logging.getLogger(__name__)

async def optimize_grid_region(region: str = "default") -> Dict[str, Any]:
    """
    Async wrapper for grid optimization compatible with NAT.
    
    Args:
        region: Grid region to optimize
        
    Returns:
        Dictionary with optimization results
    """
    try:
        # Validate region access
        if not validate_region_access(region):
            return {
                "status": "error",
                "message": f"Access denied for region: {region}",
                "region": region,
                "timestamp": datetime.now().isoformat()
            }
        
        # Run optimization in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, sync_optimize_grid, region)
        
        # Enhance result with additional metadata
        enhanced_result = {
            "status": "success",
            "region": region,
            "timestamp": datetime.now().isoformat(),
            "optimization_time": result.get("time", "N/A"),
            "loss_reduction": result.get("loss_reduction", 0),
            "optimal_config": result.get("optimal_supply", "N/A"), 
            "cost_savings": result.get("cost_savings", 0),
            "next_maintenance": result.get("next_maintenance", "Not scheduled"),
            "raw_result": result
        }
        
        return enhanced_result
        
    except Exception as e:
        logger.error(f"Grid optimization failed for region {region}: {e}")
        return {
            "status": "error",
            "message": str(e),
            "region": region,
            "timestamp": datetime.now().isoformat()
        }


async def get_optimization_status(region: str = "default") -> Dict[str, Any]:
    """
    Get current grid status and optimization history for a region.
    
    Args:
        region: Grid region to check
        
    Returns:
        Dictionary with status information
    """
    try:
        # Get database session
        engine = get_engine()
        session = get_session(engine)
        
        # Query latest grid state
        latest_state = session.query(GridState).filter(
            GridState.region == region
        ).order_by(GridState.timestamp.desc()).first()
        
        # Query recent optimizations
        recent_optimizations = session.query(OptimizationResult).filter(
            OptimizationResult.region == region
        ).order_by(OptimizationResult.timestamp.desc()).limit(5).all()
        
        if not latest_state:
            return {
                "status": "error",
                "message": f"No data found for region: {region}",
                "region": region
            }
        
        # Calculate status metrics
        efficiency = getattr(latest_state, 'efficiency', None)
        if efficiency is None and latest_state.supply and latest_state.demand:
            # Calculate efficiency if not stored
            efficiency = (latest_state.supply - latest_state.losses) / latest_state.supply * 100
        
        # Get alert count (mock implementation)
        active_alerts = 0
        if efficiency and efficiency < 85:
            active_alerts += 1
        if latest_state.current_load and latest_state.current_load > 1000:
            active_alerts += 1
            
        # Format last optimization time
        last_optimization = "Never"
        next_scheduled = "Not scheduled"
        if recent_optimizations:
            last_opt = recent_optimizations[0]
            last_optimization = last_opt.timestamp.strftime("%Y-%m-%d %H:%M")
            # Mock next scheduled time (24 hours after last)
            next_scheduled = "2024-08-15 02:00"
        
        status_data = {
            "current_status": "Operational" if efficiency and efficiency > 80 else "Attention Required",
            "region": region,
            "current_load": getattr(latest_state, 'current_load', latest_state.demand),
            "total_capacity": getattr(latest_state, 'capacity', latest_state.supply * 1.2),  # Mock capacity
            "efficiency": f"{efficiency:.1f}" if efficiency else "N/A",
            "active_alerts": active_alerts,
            "last_optimization": last_optimization,
            "next_scheduled": next_scheduled,
            "timestamp": datetime.now().isoformat(),
            "data_points": len(recent_optimizations)
        }
        
        session.close()
        return status_data
        
    except Exception as e:
        logger.error(f"Status check failed for region {region}: {e}")
        return {
            "status": "error",
            "message": str(e),
            "region": region,
            "timestamp": datetime.now().isoformat()
        }


async def analyze_grid_metrics(region: str = "default", metric: str = "efficiency") -> Dict[str, Any]:
    """
    Analyze specific grid performance metrics.
    
    Args:
        region: Grid region to analyze
        metric: Metric to focus on ('efficiency', 'load', 'capacity', 'losses')
        
    Returns:
        Dictionary with analysis results
    """
    try:
        engine = get_engine()
        session = get_session(engine)
        
        # Get historical data for analysis
        historical_data = session.query(GridState).filter(
            GridState.region == region
        ).order_by(GridState.timestamp.desc()).limit(20).all()
        
        if not historical_data:
            return {
                "status": "error",
                "message": f"No historical data for region: {region}",
                "region": region
            }
        
        analysis_result = {
            "region": region,
            "metric": metric,
            "timestamp": datetime.now().isoformat(),
            "data_points": len(historical_data)
        }
        
        if metric.lower() == "efficiency":
            efficiencies = []
            for state in historical_data:
                if hasattr(state, 'efficiency') and state.efficiency:
                    efficiencies.append(state.efficiency)
                elif state.supply and state.losses:
                    eff = (state.supply - state.losses) / state.supply * 100
                    efficiencies.append(eff)
            
            if efficiencies:
                current_eff = efficiencies[0]
                avg_eff = sum(efficiencies) / len(efficiencies)
                trend = "improving" if len(efficiencies) > 1 and efficiencies[0] > efficiencies[-1] else "stable"
                
                analysis_result.update({
                    "current_efficiency": f"{current_eff:.1f}%",
                    "average_efficiency": f"{avg_eff:.1f}%",
                    "trend": trend,
                    "target_efficiency": "95%",
                    "status": "excellent" if avg_eff > 90 else "needs_optimization"
                })
        
        elif metric.lower() == "load":
            loads = [state.current_load or state.demand for state in historical_data if state.current_load or state.demand]
            if loads:
                current_load = loads[0]
                avg_load = sum(loads) / len(loads)
                max_load = max(loads)
                load_factor = (avg_load / max_load * 100) if max_load > 0 else 0
                
                analysis_result.update({
                    "current_load": f"{current_load:.1f} MW",
                    "average_load": f"{avg_load:.1f} MW",
                    "peak_load": f"{max_load:.1f} MW", 
                    "load_factor": f"{load_factor:.1f}%",
                    "utilization": "normal" if avg_load < max_load * 0.8 else "high"
                })
        
        else:
            analysis_result["message"] = f"Analysis completed for metric: {metric}"
        
        session.close()
        return analysis_result
        
    except Exception as e:
        logger.error(f"Grid analysis failed for region {region}: {e}")
        return {
            "status": "error", 
            "message": str(e),
            "region": region,
            "timestamp": datetime.now().isoformat()
        }