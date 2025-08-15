"""
Test server module for API testing.
This creates a simplified server without the lifespan context manager for testing.
"""

import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import os

# Import our fallback runtime directly
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))
from grid_core.runtime_fallback import AIQRuntime, Config

# Create a simple app without lifespan for testing
app = FastAPI(
    title="Grid Optimization API (Test)",
    description="Test version of AI-powered grid optimization API",
    version="1.0.0-test",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize runtime synchronously for testing
config = Config.from_file("test/workflow.yml")
runtime = AIQRuntime(config)

# For testing, we'll initialize the runtime immediately
import asyncio


async def init_runtime():
    await runtime.initialize()


# Try to initialize runtime
try:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # If loop is already running, create a task
        asyncio.create_task(init_runtime())
    else:
        # If no loop is running, run it
        loop.run_until_complete(init_runtime())
except Exception as e:
    logger.warning(f"Could not initialize runtime: {e}")


# Request/Response Models
class GridOptimizationRequest(BaseModel):
    input: str
    region: Optional[str] = None


class GridOptimizationResponse(BaseModel):
    response: str
    success: bool
    metadata: Optional[dict] = None


@app.post("/ask", response_model=GridOptimizationResponse)
async def ask_grid_agent(request: GridOptimizationRequest):
    """Process grid optimization requests through the AI agent."""
    try:
        if not runtime:
            raise HTTPException(status_code=503, detail="Runtime not initialized")

        # Prepare the input with region context if provided
        user_input = request.input
        if request.region:
            user_input = f"For region {request.region}: {user_input}"

        logger.info(f"Processing request: {user_input}")

        # Execute the workflow through AIQ Runtime
        result = await runtime.run_workflow(
            workflow_name="workflow", input_data={"query": user_input}
        )

        # Extract response from result
        response_text = result.get("output", "No response generated")
        metadata = {
            "region": request.region,
            "tokens_used": result.get("tokens_used", 0),
            "execution_time": result.get("execution_time", 0),
        }

        logger.info(f"Request processed successfully")

        return GridOptimizationResponse(response=response_text, success=True, metadata=metadata)

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "runtime_initialized": runtime is not None,
        "version": "1.0.0-test",
    }


@app.get("/metrics")
async def metrics():
    """Basic metrics endpoint."""
    if not runtime:
        return {"error": "Runtime not initialized"}

    return {
        "runtime_status": "active",
        "agents_loaded": len(runtime.agents) if hasattr(runtime, "agents") else 0,
        "uptime": "active",
    }


@app.post("/optimize/{region}")
async def optimize_region(region: str):
    """Directly optimize a specific grid region."""
    try:
        if not runtime:
            raise HTTPException(status_code=503, detail="Runtime not initialized")

        input_text = f"Optimize the grid for region {region}"

        result = await runtime.run_workflow(
            workflow_name="workflow", input_data={"query": input_text}
        )

        return {"region": region, "optimization_result": result.get("output"), "success": True}

    except Exception as e:
        logger.error(f"Error optimizing region {region}: {e}")
        raise HTTPException(status_code=500, detail=f"Optimization error: {str(e)}")


@app.get("/status/{region}")
async def get_region_status(region: str):
    """Get the latest optimization status for a region."""
    try:
        if not runtime:
            raise HTTPException(status_code=503, detail="Runtime not initialized")

        input_text = f"Show the last optimization result for region {region}"

        result = await runtime.run_workflow(
            workflow_name="workflow", input_data={"query": input_text}
        )

        return {"region": region, "status": result.get("output"), "success": True}

    except Exception as e:
        logger.error(f"Error getting status for region {region}: {e}")
        raise HTTPException(status_code=500, detail=f"Status error: {str(e)}")
