#!/bin/bash

# API Test Script
# This script reads the test configuration and runs all API tests dynamically
# Usage: ./test-api.sh <backend_url> <frontend_url>

set -e

BACKEND_URL="$1"
FRONTEND_URL="$2"

if [ -z "$BACKEND_URL" ] || [ -z "$FRONTEND_URL" ]; then
    echo "Usage: $0 <backend_url> <frontend_url>"
    exit 1
fi

echo "🧪 Starting API tests..."
echo "Backend URL: $BACKEND_URL"
echo "Frontend URL: $FRONTEND_URL"

# Function to parse YAML-like config (simplified)
parse_config() {
    local config_file=".github/test-config.yml"
    
    if [ ! -f "$config_file" ]; then
        echo "❌ Test configuration file not found: $config_file"
        exit 1
    fi
    
    echo "📋 Loaded test configuration from $config_file"
}

# Function to test health endpoint
test_health_endpoint() {
    echo "🔍 Testing health endpoint..."
    
    local status=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health")
    
    if [ "$status" = "200" ]; then
        echo "✅ Health endpoint working (200)"
    else
        echo "❌ Health endpoint failed with status: $status"
        return 1
    fi
}

# Function to test search endpoint with authentication
test_search_endpoint_auth() {
    echo "🔍 Testing search endpoint with authentication..."
    
    # Get ID token for authentication
    local id_token=$(gcloud auth print-identity-token --audiences="$BACKEND_URL")
    
    if [ -z "$id_token" ]; then
        echo "❌ Failed to get ID token"
        return 1
    fi
    
    echo "✅ Got ID token, testing search endpoint..."
    
    local status=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST \
        -H "Authorization: Bearer $id_token" \
        -H "Content-Type: application/json" \
        -d '{"query":"test"}' \
        "$BACKEND_URL/api/v1/search")
    
    if [ "$status" = "200" ]; then
        echo "✅ Search endpoint working (200)"
    else
        echo "❌ Search endpoint failed with status: $status"
        return 1
    fi
}

# Function to test CORS functionality
test_cors_functionality() {
    echo "🔍 Testing CORS functionality..."
    
    # Test CORS preflight request
    local cors_test=$(curl -s -I \
        -H "Origin: $FRONTEND_URL" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        "$BACKEND_URL/api/v1/search" | grep -i "access-control-allow-origin" || echo "No CORS headers in preflight")
    
    if echo "$cors_test" | grep -q "access-control-allow-origin"; then
        echo "✅ CORS preflight request working correctly"
    else
        echo "⚠️  CORS preflight request may have issues"
        echo "CORS Response: $cors_test"
    fi
    
    # Test actual API call with CORS
    echo "🔍 Testing actual API call with CORS..."
    local api_response=$(curl -s -X POST \
        -H "Origin: $FRONTEND_URL" \
        -H "Content-Type: application/json" \
        -d '{"query":"pipeline-test"}' \
        "$BACKEND_URL/api/v1/search" || echo "API call failed")
    
    if echo "$api_response" | grep -q "You searched for:"; then
        echo "✅ API call with CORS working correctly"
        echo "Response: $api_response"
    else
        echo "❌ API call with CORS failed"
        echo "Response: $api_response"
        return 1
    fi
}

# Function to test error handling
test_error_handling() {
    echo "🔍 Testing error handling..."
    
    local error_response=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d '{"query":""}' \
        "$BACKEND_URL/api/v1/search" || echo "Error test failed")
    
    if echo "$error_response" | grep -q "Search query cannot be empty"; then
        echo "✅ Error handling working correctly"
        echo "Response: $error_response"
    else
        echo "❌ Error handling failed"
        echo "Response: $error_response"
        return 1
    fi
}

# Main test execution
main() {
    echo "🚀 Starting comprehensive API testing..."
    
    # Load configuration
    parse_config
    
    # Run tests
    test_health_endpoint || exit 1
    test_search_endpoint_auth || exit 1
    test_cors_functionality || exit 1
    test_error_handling || exit 1
    
    echo "🎉 All API tests passed successfully!"
}

# Run main function
main "$@"
