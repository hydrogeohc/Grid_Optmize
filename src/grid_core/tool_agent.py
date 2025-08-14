from aiqtoolkit.agent import Agent
from aiqtoolkit.tool_registry import ToolRegistry

# Import your registered tools
from grid_opt.security import get_secret, secure_connection
from grid_opt.operations import optimize_grid, get_latest_optimization

# Create and populate the tool registry
tool_registry = ToolRegistry()
tool_registry.register(get_secret)
tool_registry.register(secure_connection)
tool_registry.register(optimize_grid)
tool_registry.register(get_latest_optimization)

# Instantiate the agent with the tool registry
agent = Agent(
    tool_registry=tool_registry,
    # You can specify additional arguments such as llm, memory, etc.
)

# Example usage: run a prompt through the agent
if __name__ == "__main__":
    prompt = "Establish a secure connection to the MCP server and optimize the grid."
    result = agent.run(prompt)
    print(result)
