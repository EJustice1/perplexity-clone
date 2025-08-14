#!/bin/bash

# Concurrent Test Runner for Frontend and Backend
# This script runs both frontend and backend tests simultaneously

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Function to run backend tests
run_backend_tests() {
    print_status "Running backend tests..."
    cd backend
    
    # Check if Python 3.11 is available
    if command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    else
        print_error "Python 3 not found!"
        return 1
    fi
    
    # Run tests using the configuration from pyproject.toml
    $PYTHON_CMD -m pytest tests/ -v
    
    cd ..
}

# Function to run frontend tests
run_frontend_tests() {
    print_status "Running frontend tests..."
    cd frontend
    
    # Check if npm is available
    if ! command -v npm &> /dev/null; then
        print_error "npm not found!"
        return 1
    fi
    
    # Run linting (since there are no test scripts)
    print_status "Running ESLint..."
    npm run lint
    
    # Check if there are any test files
    if [ -d "tests" ] || [ -f "jest.config.js" ] || [ -f "vitest.config.js" ]; then
        print_status "Running frontend tests..."
        npm test
    else
        print_warning "No test configuration found for frontend. Running linting only."
    fi
    
    cd ..
}

# Function to run all tests concurrently
run_all_tests() {
    print_header "Starting Concurrent Test Run"
    
    # Create temporary files for output
    BACKEND_OUTPUT=$(mktemp)
    FRONTEND_OUTPUT=$(mktemp)
    
    # Run backend tests in background
    print_status "Starting backend tests in background..."
    run_backend_tests > "$BACKEND_OUTPUT" 2>&1 &
    BACKEND_PID=$!
    
    # Run frontend tests in background
    print_status "Starting frontend tests in background..."
    run_frontend_tests > "$FRONTEND_OUTPUT" 2>&1 &
    FRONTEND_PID=$!
    
    # Wait for both processes to complete
    print_status "Waiting for tests to complete..."
    wait $BACKEND_PID
    BACKEND_EXIT_CODE=$?
    
    wait $FRONTEND_PID
    FRONTEND_EXIT_CODE=$?
    
    # Display results
    print_header "Test Results"
    
    echo -e "\n${BLUE}Backend Tests:${NC}"
    if [ $BACKEND_EXIT_CODE -eq 0 ]; then
        print_success "Backend tests PASSED"
        cat "$BACKEND_OUTPUT"
    else
        print_error "Backend tests FAILED"
        cat "$BACKEND_OUTPUT"
    fi
    
    echo -e "\n${BLUE}Frontend Tests:${NC}"
    if [ $FRONTEND_EXIT_CODE -eq 0 ]; then
        print_success "Frontend tests PASSED"
        cat "$FRONTEND_OUTPUT"
    else
        print_error "Frontend tests FAILED"
        cat "$FRONTEND_OUTPUT"
    fi
    
    # Clean up temporary files
    rm "$BACKEND_OUTPUT" "$FRONTEND_OUTPUT"
    
    # Determine overall success
    if [ $BACKEND_EXIT_CODE -eq 0 ] && [ $FRONTEND_EXIT_CODE -eq 0 ]; then
        print_success "All tests PASSED! 🎉"
        exit 0
    else
        print_error "Some tests FAILED! ❌"
        exit 1
    fi
}

# Function to run tests sequentially (for debugging)
run_tests_sequential() {
    print_header "Running Tests Sequentially"
    
    print_status "Running backend tests first..."
    if run_backend_tests; then
        print_success "Backend tests completed successfully"
    else
        print_error "Backend tests failed"
        exit 1
    fi
    
    print_status "Running frontend tests..."
    if run_frontend_tests; then
        print_success "Frontend tests completed successfully"
    else
        print_error "Frontend tests failed"
        exit 1
    fi
    
    print_success "All tests completed successfully! 🎉"
}

# Main script logic
main() {
    case "${1:-concurrent}" in
        "concurrent"|"c")
            run_all_tests
            ;;
        "sequential"|"s")
            run_tests_sequential
            ;;
        "backend"|"b")
            run_backend_tests
            ;;
        "frontend"|"f")
            run_frontend_tests
            ;;
        "help"|"h"|"-h"|"--help")
            echo "Usage: $0 [option]"
            echo ""
            echo "Options:"
            echo "  concurrent (default) - Run all tests concurrently"
            echo "  sequential           - Run tests sequentially"
            echo "  backend              - Run only backend tests"
            echo "  frontend             - Run only frontend tests"
            echo "  help                 - Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                   # Run all tests concurrently"
            echo "  $0 sequential        # Run tests sequentially"
            echo "  $0 backend           # Run only backend tests"
            echo "  $0 frontend          # Run only frontend tests"
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
