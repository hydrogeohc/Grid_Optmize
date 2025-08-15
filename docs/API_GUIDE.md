# Grid Optimization API Guide

Complete guide to using the Grid Optimization REST API.

## Overview

The Grid Optimization API provides RESTful endpoints for real-time power grid optimization, status monitoring, and analytics. Built with FastAPI, it offers automatic documentation, validation, and high performance.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required for local development. For production deployments, implement appropriate authentication mechanisms.

## Response Format

All API responses follow a consistent JSON format:

```json
{
  "status": "success|error",
  "data": { ... },
  "timestamp": "2025-01-14T10:30:00Z"
}
```

## Endpoints

### Grid Operations

#### POST /grid/optimize
**Optimize power grid for a specific region**

**Request Body:**
```json
{
  "region": "us-west",
  "parameters": {
    "max_iterations": 100,
    "tolerance": 1e-6
  }
}
```

**Response:**
```json
{
  "region": "us-west",
  "status": "success",
  "optimized_supply": 1010.00,
  "optimized_demand": 1010.00,
  "losses": 4.57e-12,
  "efficiency": 99.99,
  "cost_savings": 25000,
  "timestamp": "2025-01-14T10:30:00Z",
  "optimization_time": 0.01
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/grid/optimize" \
     -H "Content-Type: application/json" \
     -d '{"region": "us-west"}'
```

#### POST /grid/optimize/async
**Start asynchronous grid optimization**

Returns a task ID for tracking long-running optimizations.

**Response:**
```json
{
  "task_id": "uuid-string",
  "region": "us-west",
  "status": "started",
  "message": "Optimization started in background"
}
```

#### GET /grid/status/{region}
**Get current grid status and optimization history**

**Response:**
```json
{
  "region": "us-west",
  "current_status": "Operational",
  "current_load": 950.5,
  "total_capacity": 1212.0,
  "efficiency": "99.1%",
  "active_alerts": 0,
  "last_optimization": "2025-01-14T10:30:00Z",
  "next_scheduled": "Not scheduled"
}
```

#### GET /grid/regions
**List all available regions**

**Response:**
```json
[
  {
    "name": "us-west",
    "display_name": "US West",
    "description": "Western United States grid",
    "capacity": 1500.0,
    "status": "active"
  },
  ...
]
```

#### GET /grid/history/{region}
**Get optimization history for a region**

**Query Parameters:**
- `limit` (optional): Maximum number of entries (default: 10)

**Response:**
```json
[
  {
    "id": 1,
    "region": "us-west",
    "timestamp": "2025-01-14T10:30:00Z",
    "supply": 1010.0,
    "demand": 1010.0,
    "losses": 4.57e-12,
    "efficiency": 99.99,
    "cost_savings": 25000
  }
]
```

### Health and Monitoring

#### GET /health
**Comprehensive health check**

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-01-14T10:30:00Z",
  "database_connected": true,
  "components": {
    "database": "healthy",
    "grid_optimization": "available",
    "nat_integration": "available",
    "configuration": "loaded (development)"
  }
}
```

#### GET /ready
**Kubernetes readiness probe**

Returns 200 if service is ready to accept requests, 503 if not ready.

#### GET /live
**Kubernetes liveness probe**

Returns 200 if service is alive.

### Information

#### GET /
**Root endpoint with API information**

#### GET /info
**Detailed API information and capabilities**

## Error Handling

### Error Response Format
```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "status_code": 400,
  "timestamp": "2025-01-14T10:30:00Z"
}
```

### Common Error Codes
- **400 Bad Request**: Invalid region or malformed request
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server processing error
- **503 Service Unavailable**: Service not ready

## Rate Limiting

Default rate limiting is set to 60 requests per minute per IP address. This can be configured in the application settings.

## Examples

### Python Client Example
```python
import requests

# Optimize grid
response = requests.post(
    "http://localhost:8000/grid/optimize",
    json={"region": "us-west"}
)
result = response.json()
print(f"Supply: {result['optimized_supply']} MW")

# Check status
status = requests.get("http://localhost:8000/grid/status/us-west")
print(status.json())
```

### JavaScript Client Example
```javascript
// Optimize grid
const response = await fetch('http://localhost:8000/grid/optimize', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ region: 'us-west' })
});

const result = await response.json();
console.log(`Supply: ${result.optimized_supply} MW`);
```

## Interactive Documentation

The API provides interactive documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces allow you to explore the API, test endpoints, and see detailed schema information.

## SDKs and Libraries

Currently, no official SDKs are available. The API follows REST conventions and can be used with any HTTP client library.

## Support

For API support:
1. Check the interactive documentation at `/docs`
2. Review error messages and status codes
3. Run health checks to verify service status
4. Check logs for detailed error information