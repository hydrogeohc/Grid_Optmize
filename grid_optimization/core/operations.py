"""
Grid optimization operations using SciPy for power loss minimization.

This module provides the core optimization algorithms for the grid optimization system,
including supply optimization and result storage functionality.
"""

from scipy.optimize import minimize

from .database import GridState, OptimizationResult, get_engine, get_session


def register_tool(name):
    """Simple decorator to register tools without AIQ toolkit dependency."""

    def decorator(func):
        func._tool_name = name
        return func

    return decorator


@register_tool("optimize_grid")
def optimize_grid(region=None):
    """
    Optimize the grid supply for a given region to minimize losses.

    Args:
        region (str, optional): The grid region to optimize. Defaults to None.

    Returns:
        dict: Optimization results including region, optimized supply, demand, and losses.
    """
    # Connect to the database and get the latest grid state
    engine = get_engine()
    session = get_session(engine)
    query = session.query(GridState)
    if region:
        query = query.filter(GridState.region == region)
    state = query.order_by(GridState.timestamp.desc()).first()
    session.close()

    if not state:
        return {"error": "No grid state data found."}

    demand = state.demand
    supply = state.supply

    # Objective: minimize (supply - demand)^2 (i.e., minimize imbalance/loss)
    def objective(x):
        return (x - demand) ** 2

    res = minimize(objective, supply)
    optimized_supply = float(res.x[0])
    losses = (optimized_supply - demand) ** 2

    # Store the optimization result
    engine = get_engine()
    session = get_session(engine)
    opt_result = OptimizationResult(
        region=state.region,
        optimized_supply=optimized_supply,
        optimized_demand=demand,
        losses=losses,
    )
    session.add(opt_result)
    session.commit()
    session.close()

    return {
        "region": state.region,
        "optimized_supply": optimized_supply,
        "optimized_demand": demand,
        "losses": losses,
    }


@register_tool("get_latest_optimization")
def get_latest_optimization(region=None):
    """
    Retrieve the latest optimization result for a given region.

    Args:
        region (str, optional): The grid region to query. Defaults to None.

    Returns:
        dict: Latest optimization result or error message.
    """
    engine = get_engine()
    session = get_session(engine)
    query = session.query(OptimizationResult)
    if region:
        query = query.filter(OptimizationResult.region == region)
    latest = query.order_by(OptimizationResult.timestamp.desc()).first()
    session.close()

    if latest:
        return {
            "region": latest.region,
            "optimized_supply": latest.optimized_supply,
            "optimized_demand": latest.optimized_demand,
            "losses": latest.losses,
            "timestamp": latest.timestamp.isoformat(),
        }
    else:
        return {"error": "No optimization result found."}
