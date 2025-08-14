#!/usr/bin/env python3
"""
NAT Workflow Usage Examples
Complete guide for interacting with your deployed Grid Optimization NAT service
"""

import requests
import json
from typing import Dict, Any

# Base URL for your NAT service
BASE_URL = "http://localhost:8001"

class GridOptimizationClient:
    """Client for interacting with the Grid Optimization NAT workflow"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the service is healthy"""
        response = self.session.get(f"{self.base_url}/health")
        return response.json()
    
    def chat(self, message: str, region: str = None) -> Dict[str, Any]:
        """
        Use the NAT chat interface (Recommended approach)
        
        Args:
            message: Natural language message
            region: Optional region filter
        """
        payload = {"message": message}
        if region:
            payload["region"] = region
            
        response = self.session.post(f"{self.base_url}/chat", json=payload)
        return response.json()
    
    def optimize_grid(self, region: str = None) -> Dict[str, Any]:
        """Direct API call to optimize the grid"""
        payload = {}
        if region:
            payload["region"] = region
            
        response = self.session.post(f"{self.base_url}/api/optimize", json=payload)
        return response.json()
    
    def get_status(self, region: str = None) -> Dict[str, Any]:
        """Get optimization status/history"""
        url = f"{self.base_url}/api/status"
        if region:
            url += f"?region={region}"
            
        response = self.session.get(url)
        return response.json()
    
    def workflow_invoke(self, input_text: str) -> Dict[str, Any]:
        """
        NAT workflow compatible interface
        
        Args:
            input_text: Input for the workflow
        """
        payload = {"input": input_text}
        response = self.session.post(f"{self.base_url}/workflow/invoke", json=payload)
        return response.json()


def demonstrate_usage():
    """Demonstrate different ways to use the NAT workflow"""
    client = GridOptimizationClient()
    
    print("🚀 Grid Optimization NAT Workflow Usage Examples")
    print("=" * 60)
    
    # 1. Health Check
    print("\n1. 🏥 Health Check")
    print("-" * 30)
    try:
        health = client.health_check()
        print(f"✅ Service Status: {health.get('status')}")
        print(f"📊 Service: {health.get('service')}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # 2. Chat Interface Examples
    print("\n2. 💬 NAT Chat Interface (Recommended)")
    print("-" * 30)
    
    # Get help
    help_response = client.chat("help")
    print("Help Response:")
    print(f"🤖 {help_response.get('response')}")
    
    # Optimize grid
    print("\nOptimization Request:")
    opt_response = client.chat("optimize the grid")
    print(f"🤖 {opt_response.get('response')}")
    if opt_response.get('data'):
        data = opt_response['data']
        print(f"📊 Region: {data.get('region')}")
        print(f"⚡ Supply: {data.get('optimized_supply', 0):.2f}")
        print(f"📈 Demand: {data.get('optimized_demand', 0):.2f}")
        print(f"💥 Losses: {data.get('losses', 0):.6f}")
    
    # Show status
    print("\nStatus Check:")
    status_response = client.chat("show last optimization")
    print(f"🤖 {status_response.get('response')}")
    
    # 3. Direct API Examples
    print("\n3. 🔗 Direct API Endpoints")
    print("-" * 30)
    
    # Direct optimization
    print("Direct Optimization:")
    direct_opt = client.optimize_grid()
    if 'error' not in direct_opt:
        print(f"✅ Optimized - Region: {direct_opt.get('region')}")
        print(f"⚡ Supply: {direct_opt.get('optimized_supply', 0):.2f}")
        print(f"📈 Demand: {direct_opt.get('optimized_demand', 0):.2f}")
    else:
        print(f"❌ {direct_opt.get('error')}")
    
    # Get status
    print("\nDirect Status Check:")
    status = client.get_status()
    if 'error' not in status:
        print(f"📊 Last optimization: {status.get('timestamp')}")
        print(f"🌍 Region: {status.get('region')}")
        print(f"💥 Losses: {status.get('losses', 0):.6f}")
    else:
        print(f"❌ {status.get('error')}")
    
    # 4. NAT Workflow Interface
    print("\n4. 🔄 NAT Workflow Compatible Interface")
    print("-" * 30)
    
    workflow_response = client.workflow_invoke("optimize the grid for us-west")
    print(f"🤖 Output: {workflow_response.get('output')}")
    
    metadata = workflow_response.get('metadata', {})
    print(f"🛠️  Workflow Type: {metadata.get('workflow_type')}")
    print(f"🔧 Tools Used: {', '.join(metadata.get('tools_used', []))}")
    
    print("\n✅ All demonstrations completed!")
    print("🌐 Visit http://localhost:8001/docs for interactive API explorer")


def example_integration():
    """Example of integrating NAT workflow into your application"""
    
    print("\n" + "="*60)
    print("🔌 Integration Example")
    print("="*60)
    
    client = GridOptimizationClient()
    
    # Simulation of a monitoring system
    print("\n📊 Grid Monitoring System Integration:")
    
    # Check system health
    if client.health_check().get('status') == 'healthy':
        print("✅ Grid optimization service is healthy")
        
        # Periodic optimization
        print("🔄 Running periodic optimization...")
        result = client.chat("optimize the grid")
        
        if result.get('data') and 'error' not in result['data']:
            losses = result['data'].get('losses', 0)
            
            if losses > 0.01:  # 1% loss threshold
                print(f"⚠️  High losses detected: {losses:.4f}")
                print("🚨 Alert: Grid requires attention!")
            else:
                print(f"✅ Grid operating efficiently - Losses: {losses:.6f}")
        
        # Get historical data
        status = client.get_status()
        if status.get('timestamp'):
            print(f"📅 Last optimization: {status['timestamp']}")
    else:
        print("❌ Grid optimization service is down!")


if __name__ == "__main__":
    print("Starting NAT Workflow demonstrations...")
    
    try:
        demonstrate_usage()
        example_integration()
        
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("Make sure your NAT service is running at http://localhost:8001")
        print("Start it with: python deploy.py")