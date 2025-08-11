#!/bin/bash

# =============================================================================
# MONITORING SETUP SCRIPT FOR PERPLEXITY CLONE
# =============================================================================
# 
# This script sets up Prometheus and Grafana monitoring for your application
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Function to create necessary directories
create_directories() {
    log_step "Creating monitoring directories..."
    
    mkdir -p prometheus
    mkdir -p grafana/provisioning/datasources
    mkdir -p grafana/dashboards
    
    log_info "Directories created successfully"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        log_error "Docker is not running or not accessible"
        exit 1
    fi
    log_info "Docker is running"
}

# Function to check if docker-compose is available
check_docker_compose() {
    if ! command -v docker-compose > /dev/null 2>&1; then
        log_error "docker-compose is not installed or not in PATH"
        exit 1
    fi
    log_info "docker-compose is available"
}

# Function to start monitoring services
start_monitoring() {
    log_step "Starting monitoring services..."
    
    # Start only monitoring services
    docker-compose up -d prometheus grafana
    
    log_info "Monitoring services started"
    log_info "Waiting for services to be ready..."
    sleep 10
}

# Function to check service health
check_services() {
    log_step "Checking service health..."
    
    # Check Prometheus
    if curl -f http://localhost:9090/-/healthy > /dev/null 2>&1; then
        log_info "✅ Prometheus is healthy"
    else
        log_error "❌ Prometheus health check failed"
    fi
    
    # Check Grafana
    if curl -f http://localhost:3000/api/health > /dev/null 2>&1; then
        log_info "✅ Grafana is healthy"
    else
        log_error "❌ Grafana health check failed"
    fi
}

# Function to show access information
show_access_info() {
    log_step "Monitoring Stack Access Information:"
    echo ""
    echo -e "${GREEN}Prometheus:${NC}"
    echo "  URL: http://localhost:9090"
    echo "  Status: http://localhost:9090/-/healthy"
    echo ""
    echo -e "${GREEN}Grafana:${NC}"
    echo "  URL: http://localhost:3000"
    echo "  Username: admin"
    echo "  Password: admin"
    echo ""
    echo -e "${GREEN}Application Endpoints:${NC}"
    echo "  Backend: http://localhost:8000"
    echo "  Frontend: http://localhost:5001"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "1. Open Grafana at http://localhost:3000"
    echo "2. Login with admin/admin"
    echo "3. The Prometheus datasource should be automatically configured"
    echo "4. Import the dashboard from grafana/dashboards/app-metrics.json"
    echo ""
}

# Function to stop monitoring services
stop_monitoring() {
    log_step "Stopping monitoring services..."
    docker-compose stop prometheus grafana
    log_info "Monitoring services stopped"
}

# Function to show logs
show_logs() {
    log_step "Showing monitoring service logs..."
    docker-compose logs prometheus grafana
}

# Main execution
main() {
    log_info "Setting up monitoring for Perplexity Clone"
    
    # Check prerequisites
    check_docker
    check_docker_compose
    
    # Create directories
    create_directories
    
    # Start services
    start_monitoring
    
    # Check health
    check_services
    
    # Show access info
    show_access_info
    
    log_info "Monitoring setup completed successfully!"
}

# Handle command line arguments
case "${1:-setup}" in
    "setup")
        main
        ;;
    "start")
        check_docker
        check_docker_compose
        start_monitoring
        check_services
        show_access_info
        ;;
    "stop")
        check_docker
        check_docker_compose
        stop_monitoring
        ;;
    "logs")
        check_docker
        check_docker_compose
        show_logs
        ;;
    "health")
        check_docker
        check_docker_compose
        check_services
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [setup|start|stop|logs|health|help]"
        echo ""
        echo "Commands:"
        echo "  setup  - Complete setup (default)"
        echo "  start  - Start monitoring services"
        echo "  stop   - Stop monitoring services"
        echo "  logs   - Show monitoring service logs"
        echo "  health - Check service health"
        echo "  help   - Show this help message"
        ;;
    *)
        log_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
