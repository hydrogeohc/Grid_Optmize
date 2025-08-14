from ..db import get_engine, get_session, GridState, OptimizationResult
from scipy.optimize import minimize
from typing import Optional

try:
    from nat.tool.register import register_tool
    NAT_AVAILABLE = True
except ImportError:
    # Fallback decorator if NAT is not available
    def register_tool(name):
        def decorator(func):
            func._tool_name = name
            return func
        return decorator
    NAT_AVAILABLE = False

@register_tool("nat_grid_optimization/optimize_grid")
def optimize_grid(region: Optional[str] = None) -> dict:
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


@register_tool("nat_grid_optimization/show_last_optimization")
def show_last_optimization(region: str = None) -> dict:
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