#!/bin/bash

# =============================================================================
# MONITORING TEST SCRIPT FOR PERPLEXITY CLONE
# =============================================================================
# 
# This script tests the complete monitoring stack to ensure everything is working
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

# Function to check if service is responding
check_service() {
    local name=$1
    local url=$2
    local description=$3
    
    log_step "Testing $name: $description"
    
    if curl -f -s "$url" > /dev/null 2>&1; then
        log_info "✅ $name is responding"
        return 0
    else
        log_error "❌ $name is not responding"
        return 1
    fi
}

# Function to check Prometheus targets
check_prometheus_targets() {
    log_step "Checking Prometheus targets..."
    
    local targets=$(curl -s http://localhost:9090/api/v1/targets | jq -r '.data.activeTargets[] | "\(.labels.job): \(.health)"' 2>/dev/null || echo "Failed to get targets")
    
    if [[ $targets == *"up"* ]]; then
        log_info "✅ Prometheus targets are healthy:"
        echo "$targets" | sed 's/^/  /'
    else
        log_error "❌ Prometheus targets are not healthy"
        return 1
    fi
}

# Function to check metrics collection
check_metrics() {
    log_step "Checking metrics collection..."
    
    # Test backend metrics
    if curl -s http://localhost:8000/metrics | grep -q "http_requests_total"; then
        log_info "✅ Backend metrics endpoint working"
    else
        log_error "❌ Backend metrics endpoint not working"
        return 1
    fi
    
    # Test frontend metrics
    if curl -s http://localhost:5001/metrics | grep -q "http_requests_total"; then
        log_info "✅ Frontend metrics endpoint working"
    else
        log_error "❌ Frontend metrics endpoint not working"
        return 1
    fi
}

# Function to generate test traffic
generate_test_traffic() {
    log_step "Generating test traffic for metrics..."
    
    for i in {1..10}; do
        curl -s http://localhost:8000/ > /dev/null
        curl -s http://localhost:5001/ > /dev/null
        sleep 0.2
    done
    
    log_info "✅ Generated test traffic"
}

# Function to check if metrics are being scraped
check_scraped_metrics() {
    log_step "Checking if Prometheus is collecting metrics..."
    
    # Wait a bit for scraping to happen
    sleep 5
    
    local backend_metrics=$(curl -s "http://localhost:9090/api/v1/query?query=http_requests_total{job=\"backend\"}" | jq -r '.data.result | length' 2>/dev/null || echo "0")
    local frontend_metrics=$(curl -s "http://localhost:9090/api/v1/query?query=http_requests_total{job=\"frontend\"}" | jq -r '.data.result | length' 2>/dev/null || echo "0")
    
    if [[ $backend_metrics -gt 0 ]] && [[ $frontend_metrics -gt 0 ]]; then
        log_info "✅ Prometheus is collecting metrics:"
        log_info "  Backend metrics: $backend_metrics series"
        log_info "  Frontend metrics: $frontend_metrics series"
    else
        log_error "❌ Prometheus is not collecting metrics properly"
        return 1
    fi
}

# Function to show access information
show_access_info() {
    log_step "Monitoring Stack Access Information:"
    echo ""
    echo -e "${GREEN}Prometheus:${NC}"
    echo "  URL: http://localhost:9090"
    echo "  Targets: http://localhost:9090/targets"
    echo "  Graph: http://localhost:9090/graph"
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
    echo "3. Import dashboard from grafana/dashboards/app-metrics.json"
    echo "4. View metrics in Prometheus at http://localhost:9090/graph"
}

# Main execution
main() {
    log_info "Testing Perplexity Clone Monitoring Stack"
    echo ""
    
    # Check all services are responding
    check_service "Backend" "http://localhost:8000/health" "Health endpoint"
    check_service "Frontend" "http://localhost:5001/health" "Health endpoint"
    check_service "Prometheus" "http://localhost:9090/-/healthy" "Health endpoint"
    check_service "Grafana" "http://localhost:3000/api/health" "Health endpoint"
    
    echo ""
    
    # Check metrics endpoints
    check_metrics
    
    echo ""
    
    # Check Prometheus targets
    check_prometheus_targets
    
    echo ""
    
    # Generate test traffic and check collection
    generate_test_traffic
    check_scraped_metrics
    
    echo ""
    
    # Show access information
    show_access_info
    
    log_info "Monitoring stack test completed!"
}

# Run the test
main
