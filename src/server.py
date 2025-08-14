from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import yaml
import logging
import asyncio
from contextlib import asynccontextmanager

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

try:
    from aiq.runtime import AIQRuntime
    from aiq.config import Config
    AIQ_AVAILABLE = True
except ImportError:
    from grid_core.runtime_fallback import AIQRuntime, Config
    AIQ_AVAILABLE = False
    logger.info("AIQ toolkit not available, using fallback runtime")

# Global runtime instance
runtime = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup/shutdown."""
    global runtime
    
    # Startup
    logger.info("Starting Grid Optimization Server...")
    try:
        # Load configuration
        config = Config.from_file("test/workflow.yml")
        
        # Initialize AIQ Runtime
        runtime = AIQRuntime(config)
        await runtime.initialize()
        
        logger.info("Grid Optimization Server started successfully")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Grid Optimization Server...")
    if runtime:
        await runtime.shutdown()
    logger.info("Server shutdown complete")

# Initialize FastAPI app with lifespan manager
app = FastAPI(
    title="Grid Optimization API",
    description="AI-powered grid optimization using NeMo Agent Toolkit",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class GridOptimizationRequest(BaseModel):
    input: str
    region: Optional[str] = None
    
class GridOptimizationResponse(BaseModel):
    response: str
    success: bool
    metadata: Optional[dict] = None

@app.get("/")
async def root():
    return {"message": "Grid Optimization API", "docs": "/docs", "health": "/health"}

@app.post("/ask", response_model=GridOptimizationResponse)
async def ask_grid_agent(request: GridOptimizationRequest):
    """
    Process grid optimization requests through the AI agent.
    
    Args:
        request: Grid optimization request containing user input and optional region
        
    Returns:
        GridOptimizationResponse: Agent response with optimization results
    """
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
            workflow_name="workflow",
            input_data={"query": user_input}
        )
        
        # Extract response from result
        response_text = result.get("output", "No response generated")
        metadata = {
            "region": request.region,
            "tokens_used": result.get("tokens_used", 0),
            "execution_time": result.get("execution_time", 0)
        }
        
        logger.info(f"Request processed successfully")
        
        return GridOptimizationResponse(
            response=response_text,
            success=True,
            metadata=metadata
        )
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "runtime_initialized": runtime is not None,
        "version": "1.0.0"
    }

@app.get("/metrics") 
async def metrics():
    """Basic metrics endpoint."""
    if not runtime:
        return {"error": "Runtime not initialized"}
        
    return {
        "runtime_status": "active",
        "agents_loaded": len(runtime.agents) if hasattr(runtime, 'agents') else 0,
        "uptime": "active"  # Add actual uptime tracking if needed
    }

# Additional endpoints for grid-specific operations
@app.post("/optimize/{region}")
async def optimize_region(region: str):
    """Directly optimize a specific grid region."""
    try:
        if not runtime:
            raise HTTPException(status_code=503, detail="Runtime not initialized")
            
        input_text = f"Optimize the grid for region {region}"
        
        result = await runtime.run_workflow(
            workflow_name="workflow", 
            input_data={"query": input_text}
        )
        
        return {
            "region": region,
            "optimization_result": result.get("output"),
            "success": True
        }
        
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
            workflow_name="workflow",
            input_data={"query": input_text}  
        )
        
        return {
            "region": region,
            "status": result.get("output"),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error getting status for region {region}: {e}")
        raise HTTPException(status_code=500, detail=f"Status error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    # Load app config
    try:
        with open("config.yml", "r") as f:
            config = yaml.safe_load(f)
        
        host = config.get("api", {}).get("host", "0.0.0.0")
        port = config.get("api", {}).get("port", 8000)
        
    except Exception as e:
        logger.warning(f"Could not load config: {e}. Using defaults.")
        host = "0.0.0.0" 
        port = 8000
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )