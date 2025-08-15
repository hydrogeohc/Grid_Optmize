#!/usr/bin/env python3
"""
Simple deployment script for Grid Optimization System
Combines your existing server with NAT-like capabilities
"""
import os
import sys
from typing import Optional

# Import your existing grid optimization functions
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.grid_core.tools.grid_tools import optimize_grid, show_last_optimization

app = FastAPI(
    title="Grid Optimization API",
    description="AI-powered grid optimization system with NAT-compatible interface",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data models
class ChatRequest(BaseModel):
    message: str
    region: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    data: Optional[dict] = None


class OptimizeRequest(BaseModel):
    region: Optional[str] = None


# NAT-compatible endpoints
@app.get("/")
async def root():
    return {
        "service": "Grid Optimization API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "optimize": "/api/optimize",
            "status": "/api/status",
            "health": "/health",
        },
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "grid-optimization-api"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    NAT-style chat interface for grid optimization
    """
    message = request.message.lower()
    region = request.region

    try:
        # Simple command parsing
        if "optimize" in message or "optimization" in message:
            result = optimize_grid(region=region)
            if "error" in result:
                return ChatResponse(
                    response=f"I encountered an issue: {result['error']}", data=result
                )
            return ChatResponse(
                response=f"I've optimized the grid for {result['region']}. "
                f"Optimized supply: {result['optimized_supply']:.2f}, "
                f"Demand: {result['optimized_demand']:.2f}, "
                f"Losses: {result['losses']:.4f}",
                data=result,
            )

        elif "status" in message or "last" in message or "recent" in message:
            result = show_last_optimization(region=region)
            if "error" in result:
                return ChatResponse(
                    response="No optimization results found for the specified region.", data=result
                )
            return ChatResponse(
                response=f"Last optimization for {result['region']} was on {result['timestamp']}. "
                f"Supply: {result['optimized_supply']:.2f}, "
                f"Demand: {result['optimized_demand']:.2f}, "
                f"Losses: {result['losses']:.4f}",
                data=result,
            )

        elif "help" in message:
            return ChatResponse(
                response="I can help you with grid optimization! Try asking me to:\n"
                "• 'Optimize the grid' - Run optimization for a region\n"
                "• 'Show last optimization' - View recent results\n"
                "• 'Optimize region us-west' - Optimize specific region",
                data={"commands": ["optimize", "status", "help"]},
            )

        else:
            return ChatResponse(
                response="I'm a grid optimization assistant. I can help optimize grid supply "
                "and demand to minimize losses. Ask me to 'optimize the grid' or "
                "'show last optimization'.",
                data={"suggestion": "Try saying 'optimize the grid' or 'help'"},
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.post("/api/optimize")
async def optimize_endpoint(request: OptimizeRequest):
    """Direct API endpoint for grid optimization"""
    try:
        result = optimize_grid(region=request.region)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status")
async def status_endpoint(region: Optional[str] = None):
    """Get last optimization status"""
    try:
        result = show_last_optimization(region=region)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# NAT workflow-compatible endpoint
@app.post("/workflow/invoke")
async def workflow_invoke(request: dict):
    """
    NAT-compatible workflow endpoint
    """
    try:
        input_data = request.get("input", "")

        # Route to chat handler
        chat_request = ChatRequest(message=input_data)
        response = await chat_endpoint(chat_request)

        return {
            "output": response.response,
            "metadata": {
                "data": response.data,
                "workflow_type": "grid_optimization",
                "tools_used": ["optimize_grid", "show_last_optimization"],
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("🚀 Starting Grid Optimization API with NAT-compatible interface...")
    print("📡 API will be available at: http://localhost:8001")
    print("📖 Interactive docs at: http://localhost:8001/docs")
    print("🔧 NAT-style chat endpoint: POST /chat")
    print("⚡ Direct optimization: POST /api/optimize")

    uvicorn.run("deploy:app", host="0.0.0.0", port=8001, reload=True, log_level="info")
