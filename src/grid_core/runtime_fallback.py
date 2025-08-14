"""
Fallback runtime implementation for Grid Optimization when AIQ toolkit is not available.
This provides a simple interface that matches the AIQ runtime API for testing purposes.
"""

import yaml
import logging
from typing import Dict, Any, Optional
from .tools.grid_tools import optimize_grid, show_last_optimization

logger = logging.getLogger(__name__)


class Config:
    """Simple configuration class to replace aiq.Config."""
    
    def __init__(self, config_data: dict):
        self.config_data = config_data
    
    @classmethod
    def from_file(cls, file_path: str) -> 'Config':
        """Load configuration from YAML file."""
        try:
            with open(file_path, 'r') as f:
                config_data = yaml.safe_load(f)
            return cls(config_data)
        except Exception as e:
            logger.error(f"Failed to load config from {file_path}: {e}")
            # Return a minimal default config
            return cls({
                "workflow": {"_type": "react_agent"},
                "llms": {"grid_llm": {"_type": "mock", "model_name": "mock-model"}}
            })


class AIQRuntime:
    """Simple runtime implementation to replace aiq.runtime.AIQRuntime."""
    
    def __init__(self, config: Config):
        self.config = config
        self.agents = ["grid_optimization_agent"]
        self._initialized = False
        
        # Map of available tools
        self.tools = {
            "optimize_grid": optimize_grid,
            "show_last_optimization": show_last_optimization
        }
    
    async def initialize(self):
        """Initialize the runtime."""
        logger.info("Initializing fallback AIQ runtime...")
        self._initialized = True
        logger.info("Fallback runtime initialized successfully")
    
    async def shutdown(self):
        """Shutdown the runtime."""
        logger.info("Shutting down fallback runtime...")
        self._initialized = False
    
    async def run_workflow(self, workflow_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a workflow with the given input data.
        
        Args:
            workflow_name: Name of the workflow to run
            input_data: Input data containing the query
            
        Returns:
            Dict containing the workflow results
        """
        if not self._initialized:
            raise RuntimeError("Runtime not initialized")
        
        query = input_data.get("query", "")
        logger.info(f"Processing query: {query}")
        
        # Simple query processing - determine which tool to call
        if "optimize" in query.lower():
            # Extract region if specified
            region = self._extract_region(query)
            result = optimize_grid(region)
            
            if "error" in result:
                output = f"Error: {result['error']}"
            else:
                output = f"Grid optimization completed for region {result['region']}. " \
                        f"Optimized supply: {result['optimized_supply']:.2f}, " \
                        f"Optimized demand: {result['optimized_demand']:.2f}, " \
                        f"Losses: {result['losses']:.2f}"
        
        elif "show" in query.lower() or "last" in query.lower() or "result" in query.lower():
            # Show last optimization results
            region = self._extract_region(query)
            result = show_last_optimization(region)
            
            if "error" in result:
                output = f"No optimization results found for region {region or 'default'}"
            else:
                output = f"Last optimization for region {result['region']}: " \
                        f"Supply: {result['optimized_supply']:.2f}, " \
                        f"Demand: {result['optimized_demand']:.2f}, " \
                        f"Losses: {result['losses']:.2f}, " \
                        f"Timestamp: {result['timestamp']}"
        
        else:
            output = "Grid optimization system is ready. Available commands: 'optimize grid' or 'show last results'"
        
        return {
            "output": output,
            "tokens_used": len(query) + len(output),  # Simple approximation
            "execution_time": 1.0,  # Mock execution time
            "success": True
        }
    
    def _extract_region(self, query: str) -> Optional[str]:
        """Extract region from query text."""
        query_lower = query.lower()
        
        # Common region patterns
        regions = ["us-west", "us-east", "us-central", "pgae", "pge", "socal"]
        
        for region in regions:
            if region in query_lower:
                return region
        
        # Look for "region X" pattern
        words = query.split()
        for i, word in enumerate(words):
            if word.lower() == "region" and i + 1 < len(words):
                return words[i + 1].lower()
        
        return None