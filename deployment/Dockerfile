# Use Python 3.11 for NeMo Agent Toolkit compatibility
FROM python:3.11-slim

# Install system dependencies including uv
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

# Add uv to PATH
ENV PATH="/root/.cargo/bin:$PATH"

# Set working directory
WORKDIR /app

# Create required directories
RUN mkdir -p logs data temp

# Copy Python project files
COPY pyproject.toml ./
COPY requirements.txt ./

# Install Python dependencies
RUN uv pip install --system --no-cache -r requirements.txt

# Copy configuration files first
COPY config.yml ./
COPY test/ ./test/

# Copy application code
COPY server.py ./
COPY grid_ops/ ./grid_ops/

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash gridopt && \
    chown -R gridopt:gridopt /app

USER gridopt

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Use uvicorn instead of gunicorn for FastAPI
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
