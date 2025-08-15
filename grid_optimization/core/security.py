"""
Grid Optimization Security Module
Handles authentication, authorization, and secure operations
"""

import logging
import os
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Valid grid regions for access control
VALID_REGIONS = {
    "us-west",
    "us-east",
    "us-central",
    "us-south",
    "europe",
    "asia",
    "default",
    "test-region",
}


def validate_region_access(region: str) -> bool:
    """
    Validate access to a specific grid region.

    Args:
        region: Grid region identifier

    Returns:
        True if access is allowed, False otherwise
    """
    if not region or not isinstance(region, str):
        logger.warning(f"Invalid region type: {type(region)}")
        return False

    region_clean = region.strip().lower()

    # Check against valid regions
    if region_clean in VALID_REGIONS:
        logger.info(f"Access granted to region: {region_clean}")
        return True

    # Log unauthorized access attempt
    logger.warning(f"Access denied to region: {region_clean}")
    return False


def get_secret(name: str) -> Optional[str]:
    """
    Retrieve a secret from environment variables (simplified implementation).

    Args:
        name: Secret name

    Returns:
        Secret value or None if not found
    """
    try:
        # Try environment variable first
        env_key = f"GRID_SECRET_{name.upper().replace('-', '_')}"
        secret = os.getenv(env_key)

        if secret:
            logger.info(f"Retrieved secret: {name}")
            return secret

        # Fallback to direct environment variable
        secret = os.getenv(name.upper())
        if secret:
            logger.info(f"Retrieved secret from direct env: {name}")
            return secret

        logger.warning(f"Secret not found: {name}")
        return None

    except Exception as e:
        logger.error(f"Error retrieving secret {name}: {e}")
        return None


def secure_connection(endpoint: str = "default") -> Dict[str, Any]:
    """
    Create a secure connection configuration.

    Args:
        endpoint: Connection endpoint identifier

    Returns:
        Connection configuration dictionary
    """
    try:
        # Get authentication token
        token = get_secret("mcp-token") or "default-token"

        # Get base URL from environment or use default
        base_url = os.getenv("GRID_SERVER_URL", "https://localhost:8000")

        connection_config = {
            "url": f"{base_url}/api/v1/{endpoint}",
            "headers": {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "X-Grid-Client": "nat-toolkit",
            },
            "verify_ssl": os.getenv("GRID_VERIFY_SSL", "true").lower() == "true",
            "timeout": int(os.getenv("GRID_TIMEOUT", "30")),
        }

        logger.info(f"Created secure connection config for endpoint: {endpoint}")
        return connection_config

    except Exception as e:
        logger.error(f"Error creating secure connection: {e}")
        return {
            "url": "https://localhost:8000/api/v1/default",
            "headers": {"Authorization": "Bearer default-token"},
            "verify_ssl": False,
            "timeout": 30,
        }


def validate_input(data: Any, max_length: int = 1000) -> bool:
    """
    Validate input data for security.

    Args:
        data: Input data to validate
        max_length: Maximum allowed length for string data

    Returns:
        True if input is valid, False otherwise
    """
    try:
        # Check for None or empty
        if data is None:
            return False

        # String validation
        if isinstance(data, str):
            if len(data) > max_length:
                logger.warning(f"Input too long: {len(data)} > {max_length}")
                return False

            # Basic injection prevention
            dangerous_patterns = ["<script", "javascript:", "eval(", "exec("]
            data_lower = data.lower()
            for pattern in dangerous_patterns:
                if pattern in data_lower:
                    logger.warning(f"Dangerous pattern detected: {pattern}")
                    return False

        # Dictionary validation
        elif isinstance(data, dict):
            for key, value in data.items():
                if not validate_input(key, max_length // 10):
                    return False
                if not validate_input(value, max_length):
                    return False

        # List validation
        elif isinstance(data, list):
            for item in data:
                if not validate_input(item, max_length):
                    return False

        return True

    except Exception as e:
        logger.error(f"Error validating input: {e}")
        return False


def sanitize_region_name(region: str) -> str:
    """
    Sanitize region name for safe use.

    Args:
        region: Raw region name

    Returns:
        Sanitized region name
    """
    if not region or not isinstance(region, str):
        return "default"

    # Remove dangerous characters and normalize
    sanitized = "".join(c for c in region.lower() if c.isalnum() or c in "-_")

    # Limit length
    sanitized = sanitized[:50]

    # Default if empty after sanitization
    return sanitized if sanitized else "default"
