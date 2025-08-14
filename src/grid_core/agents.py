from aiq.agents import ReactAgent
from aiq.registry import register_agent
from typing import Dict, Any


@register_agent("grid_optimization_agent")
class GridOptimizationAgent(ReactAgent):
    """
    Specialized grid optimization agent that uses NeMo-Agent-Toolkit's ReactAgent
    for intelligent grid management and optimization tasks.
    """
    
    def __init__(self, config: Dict[str, Any], **kwargs):
        """
        Initialize the Grid Optimization Agent with configuration.
        
        Args:
            config: Agent configuration dictionary
            **kwargs: Additional arguments passed to ReactAgent
        """
        super().__init__(config, **kwargs)
        self.model_path = config.get("model_path")
        self.device = config.get("device", "cuda")
        
    def get_system_prompt(self) -> str:
        """
        Returns the system prompt for the grid optimization agent.
        
        Returns:
            str: System prompt describing the agent's capabilities
        """
        return """You are a specialized Grid Optimization Agent powered by NVIDIA NeMo.
        
Your primary responsibilities include:
- Analyzing power grid states and performance metrics
- Optimizing grid supply to minimize losses and improve efficiency  
- Providing insights on grid operations and historical optimization results
- Ensuring secure and compliant grid management operations

Available tools:
- optimize_grid: Optimize grid supply for specified regions to minimize losses
- show_last_optimization: Display the most recent optimization results

Always provide clear, actionable responses about grid optimization tasks and maintain focus on power grid efficiency and reliability."""

    def preprocess_input(self, user_input: str) -> str:
        """
        Preprocess user input to better handle grid-specific terminology.
        
        Args:
            user_input: Raw user input string
            
        Returns:
            str: Preprocessed input optimized for grid operations
        """
        # Add context for grid-related queries
        input_lower = user_input.lower()
        
        if any(keyword in input_lower for keyword in ["optimize", "optimization"]):
            return f"Grid Optimization Request: {user_input}"
        elif any(keyword in input_lower for keyword in ["status", "results", "last", "recent"]):
            return f"Grid Status Query: {user_input}"
        elif any(keyword in input_lower for keyword in ["grid", "power", "supply", "demand"]):
            return f"Grid Operations Query: {user_input}"
        
        return user_input
