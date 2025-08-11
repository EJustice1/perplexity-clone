#!/bin/bash

# =============================================================================
# CI/CD BUILD SCRIPT FOR PERPLEXITY CLONE
# =============================================================================
# 
# This script handles building, testing, and optionally pushing the Docker image
# Designed for use in CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins, etc.)
# =============================================================================

set -e  # Exit on any error

# Configuration
IMAGE_NAME="perplexity-clone"
IMAGE_TAG="${IMAGE_TAG:-latest}"
REGISTRY="${REGISTRY:-}"
FULL_IMAGE_NAME="${REGISTRY}${IMAGE_NAME}:${IMAGE_TAG}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        log_error "Docker is not running or not accessible"
        exit 1
    fi
    log_info "Docker is running"
}

# Function to build the image
build_image() {
    log_info "Building Docker image: ${FULL_IMAGE_NAME}"
    
    # Build with BuildKit for better performance
    export DOCKER_BUILDKIT=1
    
    docker build \
        --target production \
        --tag "${FULL_IMAGE_NAME}" \
        --file Dockerfile \
        .
    
    if [ $? -eq 0 ]; then
        log_info "Image built successfully: ${FULL_IMAGE_NAME}"
    else
        log_error "Image build failed"
        exit 1
    fi
}

# Function to test the image
test_image() {
    log_info "Testing Docker image"
    
    # Start the container
    CONTAINER_ID=$(docker run -d -p 8000:8000 -p 5001:5001 "${FULL_IMAGE_NAME}")
    
    if [ -z "$CONTAINER_ID" ]; then
        log_error "Failed to start container"
        exit 1
    fi
    
    log_info "Container started with ID: ${CONTAINER_ID}"
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 10
    
    # Test backend health
    log_info "Testing backend health..."
    if curl -f http://localhost:8000/ > /dev/null 2>&1; then
        log_info "Backend is healthy"
    else
        log_error "Backend health check failed"
        docker logs "${CONTAINER_ID}"
        docker stop "${CONTAINER_ID}" > /dev/null 2>&1
        docker rm "${CONTAINER_ID}" > /dev/null 2>&1
        exit 1
    fi
    
    # Test frontend
    log_info "Testing frontend..."
    if curl -f http://localhost:5001/ > /dev/null 2>&1; then
        log_info "Frontend is responding"
    else
        log_error "Frontend test failed"
        docker logs "${CONTAINER_ID}"
        docker stop "${CONTAINER_ID}" > /dev/null 2>&1
        docker rm "${CONTAINER_ID}" > /dev/null 2>&1
        exit 1
    fi
    
    # Stop and remove test container
    log_info "Cleaning up test container..."
    docker stop "${CONTAINER_ID}" > /dev/null 2>&1
    docker rm "${CONTAINER_ID}" > /dev/null 2>&1
    
    log_info "Image test passed successfully"
}

# Function to push the image (if registry is specified)
push_image() {
    if [ -n "${REGISTRY}" ]; then
        log_info "Pushing image to registry: ${FULL_IMAGE_NAME}"
        
        if docker push "${FULL_IMAGE_NAME}"; then
            log_info "Image pushed successfully"
        else
            log_error "Failed to push image"
            exit 1
        fi
    else
        log_warn "No registry specified, skipping push"
    fi
}

# Function to run security scan
security_scan() {
    if command -v trivy > /dev/null 2>&1; then
        log_info "Running security scan with Trivy..."
        trivy image --severity HIGH,CRITICAL "${FULL_IMAGE_NAME}"
    else
        log_warn "Trivy not found, skipping security scan"
    fi
}

# Function to show image information
show_image_info() {
    log_info "Image information:"
    docker images "${FULL_IMAGE_NAME}"
    docker history "${FULL_IMAGE_NAME}" --no-trunc | head -20
}

# Main execution
main() {
    log_info "Starting build process for ${IMAGE_NAME}"
    
    # Check prerequisites
    check_docker
    
    # Build the image
    build_image
    
    # Test the image
    test_image
    
    # Security scan
    security_scan
    
    # Show image information
    show_image_info
    
    # Push if registry is specified
    push_image
    
    log_info "Build process completed successfully!"
}

# Handle command line arguments
case "${1:-build}" in
    "build")
        main
        ;;
    "test")
        check_docker
        test_image
        ;;
    "push")
        check_docker
        push_image
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [build|test|push|help]"
        echo ""
        echo "Commands:"
        echo "  build  - Build and test the image (default)"
        echo "  test   - Test an existing image"
        echo "  push   - Push the image to registry"
        echo "  help   - Show this help message"
        echo ""
        echo "Environment variables:"
        echo "  IMAGE_TAG  - Image tag (default: latest)"
        echo "  REGISTRY   - Docker registry URL (optional)"
        ;;
    *)
        log_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
