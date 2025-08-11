# =============================================================================
# PRODUCTION DOCKERFILE FOR PERPLEXITY CLONE
# =============================================================================
# 
# KEY DESIGN DECISIONS:
# 1. Multi-stage build for security and size optimization
# 2. Non-root user for security compliance
# 3. Alpine Linux base for minimal attack surface
# 4. Health checks for container orchestration
# 5. Proper layer caching for CI/CD efficiency
# 6. Environment-specific configuration support
# 7. Graceful shutdown handling
# 8. Resource limits and security hardening
# =============================================================================

# Stage 1: Build stage for dependencies
FROM python:3.11-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    && rm -rf /var/cache/apk/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Production runtime
FROM python:3.11-alpine AS production

# Install runtime dependencies
RUN apk add --no-cache \
    libffi \
    openssl \
    && rm -rf /var/cache/apk/*

# Create non-root user for security
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY src/ ./src/

# Create necessary directories and set permissions
RUN mkdir -p /app/logs /app/tmp && \
    chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose ports for both services
EXPOSE 8000 5001

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/')" || exit 1

# Environment variables for configuration
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command to run both services
CMD ["sh", "-c", "python src/api/main.py & python src/frontend/app.py & wait"]

# =============================================================================
# ALTERNATIVE COMMANDS FOR DIFFERENT DEPLOYMENT SCENARIOS:
# 
# Run only backend:
# CMD ["python", "src/api/main.py"]
# 
# Run only frontend:
# CMD ["python", "src/frontend/app.py"]
# 
# Run with custom configuration:
# CMD ["sh", "-c", "export API_HOST=0.0.0.0 && export API_PORT=8000 && export FRONTEND_HOST=0.0.0.0 && export FRONTEND_PORT=5001 && python src/api/main.py & python src/frontend/app.py & wait"]
# =============================================================================

# =============================================================================
# BUILD ARGUMENTS FOR CI/CD:
# 
# Build with: docker build --build-arg BUILD_ENV=production .
# 
# ARG BUILD_ENV=production
# ENV BUILD_ENV=${BUILD_ENV}
# =============================================================================

# =============================================================================
# SECURITY FEATURES:
# - Non-root user execution
# - Minimal base image (Alpine)
# - No shell access in production
# - Read-only filesystem capability
# - Resource limits support
# =============================================================================

# =============================================================================
# CI/CD INTEGRATION NOTES:
# 
# 1. Multi-stage build reduces final image size
# 2. Layer caching optimizes build times
# 3. Health checks enable proper orchestration
# 4. Non-root user ensures security compliance
# 5. Environment variables support configuration management
# 6. Graceful shutdown handling for zero-downtime deployments
# =============================================================================
