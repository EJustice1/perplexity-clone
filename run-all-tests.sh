#!/bin/bash

# Comprehensive Test Runner for Frontend and Backend
# This script runs all tests, style checks, and linting

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
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
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}================================${NC}"
}

print_subheader() {
    echo -e "${CYAN}--- $1 ---${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Function to run backend tests
run_backend_tests() {
    print_subheader "Backend Tests"
    cd backend
    
    # Check if Python 3.11 is available
    if command_exists python3.11; then
        PYTHON_CMD="python3.11"
    elif command_exists python3; then
        PYTHON_CMD="python3"
    else
        print_error "Python 3 not found!"
        return 1
    fi
    
    # Check if pytest is available
    if ! $PYTHON_CMD -c "import pytest" 2>/dev/null; then
        print_error "pytest not found! Installing..."
        pip install pytest
    fi
    
    # Run tests using the configuration from pyproject.toml
    print_status "Running pytest..."
    $PYTHON_CMD -m pytest tests/ -v --tb=short
    
    cd ..
}

# Function to run backend style checks
run_backend_style_checks() {
    print_subheader "Backend Style Checks"
    cd backend
    
    # Check if Python 3.11 is available
    if command_exists python3.11; then
        PYTHON_CMD="python3.11"
    elif command_exists python3; then
        PYTHON_CMD="python3"
    else
        print_error "Python 3 not found!"
        return 1
    fi
    
    # Check if black is available
    if ! $PYTHON_CMD -c "import black" 2>/dev/null; then
        print_warning "black not found. Skipping code formatting check."
    else
        print_status "Checking code formatting with black..."
        $PYTHON_CMD -m black --check --diff src/ tests/
    fi
    
    # Check if flake8 is available
    if ! $PYTHON_CMD -c "import flake8" 2>/dev/null; then
        print_warning "flake8 not found. Skipping linting."
    else
        print_status "Running flake8 linting..."
        $PYTHON_CMD -m flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503
    fi
    
    # Check if mypy is available
    if ! $PYTHON_CMD -c "import mypy" 2>/dev/null; then
        print_warning "mypy not found. Skipping type checking."
    else
        print_status "Running mypy type checking..."
        $PYTHON_CMD -m mypy src/ --ignore-missing-imports
    fi
    
    cd ..
}

# Function to run frontend tests
run_frontend_tests() {
    print_subheader "Frontend Tests"
    cd frontend
    
    # Check if npm is available
    if ! command_exists npm; then
        print_error "npm not found!"
        return 1
    fi
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        print_status "Installing frontend dependencies..."
        npm install
    fi
    
    # Run tests
    print_status "Running Jest tests..."
    npm test -- --passWithNoTests --watchAll=false
    
    cd ..
}

# Function to run frontend style checks
run_frontend_style_checks() {
    print_subheader "Frontend Style Checks"
    cd frontend
    
    # Check if npm is available
    if ! command_exists npm; then
        print_error "npm not found!"
        return 1
    fi
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        print_status "Installing frontend dependencies..."
        npm install
    fi
    
    # Run ESLint
    print_status "Running ESLint..."
    npm run lint
    
    # Check if Prettier is available
    if ! command_exists npx; then
        print_warning "npx not found. Skipping Prettier check."
    else
        print_status "Checking code formatting with Prettier..."
        npx prettier --check "src/**/*.{ts,tsx,js,jsx}" || print_warning "Prettier check failed or files need formatting"
    fi
    
    # Check TypeScript compilation
    print_status "Checking TypeScript compilation..."
    npx tsc --noEmit
    
    cd ..
}

# Function to run all tests and checks
run_all_tests_and_checks() {
    print_header "Starting Comprehensive Test Run"
    
    local overall_exit_code=0
    
    # Backend tests and style checks
    print_status "Running backend tests and style checks..."
    if run_backend_tests; then
        print_success "Backend tests PASSED"
    else
        print_error "Backend tests FAILED"
        overall_exit_code=1
    fi
    
    if run_backend_style_checks; then
        print_success "Backend style checks PASSED"
    else
        print_warning "Backend style checks had issues"
        # Don't fail overall for style check warnings
    fi
    
    echo ""
    
    # Frontend tests and style checks
    print_status "Running frontend tests and style checks..."
    if run_frontend_tests; then
        print_success "Frontend tests PASSED"
    else
        print_error "Frontend tests FAILED"
        overall_exit_code=1
    fi
    
    if run_frontend_style_checks; then
        print_success "Frontend style checks PASSED"
    else
        print_warning "Frontend style checks had issues"
        # Don't fail overall for style check warnings
    fi
    
    echo ""
    
    # Final results
    print_header "Final Results"
    if [ $overall_exit_code -eq 0 ]; then
        print_success "All tests PASSED! 🎉"
        print_success "Code quality checks completed successfully!"
    else
        print_error "Some tests FAILED! ❌"
        print_warning "Please fix the failing tests before proceeding."
    fi
    
    return $overall_exit_code
}

# Function to run tests sequentially (for debugging)
run_tests_sequential() {
    print_header "Running Tests Sequentially"
    
    local overall_exit_code=0
    
    print_status "Running backend tests first..."
    if run_backend_tests; then
        print_success "Backend tests completed successfully"
    else
        print_error "Backend tests failed"
        overall_exit_code=1
    fi
    
    print_status "Running backend style checks..."
    if run_backend_style_checks; then
        print_success "Backend style checks completed successfully"
    else
        print_warning "Backend style checks had issues"
    fi
    
    print_status "Running frontend tests..."
    if run_frontend_tests; then
        print_success "Frontend tests completed successfully"
    else
        print_error "Frontend tests failed"
        overall_exit_code=1
    fi
    
    print_status "Running frontend style checks..."
    if run_frontend_style_checks; then
        print_success "Frontend style checks completed successfully"
    else
        print_warning "Frontend style checks had issues"
    fi
    
    if [ $overall_exit_code -eq 0 ]; then
        print_success "All tests completed successfully! 🎉"
    else
        print_error "Some tests failed! ❌"
    fi
    
    return $overall_exit_code
}

# Function to install development dependencies
install_dev_dependencies() {
    print_header "Installing Development Dependencies"
    
    # Backend dependencies
    print_subheader "Backend Dependencies"
    cd backend
    if command_exists python3.11; then
        PYTHON_CMD="python3.11"
    elif command_exists python3; then
        PYTHON_CMD="python3"
    else
        print_error "Python 3 not found!"
        return 1
    fi
    
    print_status "Installing pytest..."
    $PYTHON_CMD -m pip install pytest
    
    print_status "Installing black..."
    $PYTHON_CMD -m pip install black
    
    print_status "Installing flake8..."
    $PYTHON_CMD -m pip install flake8
    
    print_status "Installing mypy..."
    $PYTHON_CMD -m pip install mypy
    
    cd ..
    
    # Frontend dependencies
    print_subheader "Frontend Dependencies"
    cd frontend
    if [ ! -d "node_modules" ]; then
        print_status "Installing npm dependencies..."
        npm install
    else
        print_status "npm dependencies already installed"
    fi
    cd ..
    
    print_success "Development dependencies installed successfully!"
}

# Main script logic
main() {
    case "${1:-all}" in
        "all"|"a")
            run_all_tests_and_checks
            ;;
        "sequential"|"s")
            run_tests_sequential
            ;;
        "backend"|"b")
            run_backend_tests
            run_backend_style_checks
            ;;
        "frontend"|"f")
            run_frontend_tests
            run_frontend_style_checks
            ;;
        "backend-tests"|"bt")
            run_backend_tests
            ;;
        "backend-style"|"bs")
            run_backend_style_checks
            ;;
        "frontend-tests"|"ft")
            run_frontend_tests
            ;;
        "frontend-style"|"fs")
            run_frontend_style_checks
            ;;
        "install"|"i")
            install_dev_dependencies
            ;;
        "help"|"h"|"-h"|"--help")
            echo "Usage: $0 [option]"
            echo ""
            echo "Options:"
            echo "  all (default)        - Run all tests and style checks"
            echo "  sequential           - Run tests sequentially"
            echo "  backend              - Run backend tests and style checks"
            echo "  frontend             - Run frontend tests and style checks"
            echo "  backend-tests        - Run only backend tests"
            echo "  backend-style        - Run only backend style checks"
            echo "  frontend-tests       - Run only frontend tests"
            echo "  frontend-style       - Run only frontend style checks"
            echo "  install              - Install development dependencies"
            echo "  help                 - Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                   # Run all tests and checks"
            echo "  $0 sequential        # Run tests sequentially"
            echo "  $0 backend           # Run backend tests and style checks"
            echo "  $0 frontend          # Run frontend tests and style checks"
            echo "  $0 install           # Install dev dependencies"
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
