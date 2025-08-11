# Scripts

Utility scripts for building, deploying, and managing the Perplexity Clone application.

## Available Scripts

### build.sh
Main build script for the entire application.

```bash
# Build all services
./scripts/build.sh

# Build specific service
./scripts/build.sh backend
./scripts/build.sh frontend
```

### setup-monitoring.sh
Sets up the monitoring stack (Prometheus + Grafana).

```bash
# Setup monitoring
./scripts/setup-monitoring.sh

# Verify setup
docker ps | grep -E "(prometheus|grafana)"
```

## Usage

### Prerequisites

- Docker and Docker Compose installed
- Appropriate permissions to run scripts
- Environment variables configured

### Environment Variables

```bash
# Build configuration
BUILD_ENVIRONMENT=production
DOCKER_REGISTRY=your-registry.com
IMAGE_TAG=latest

# Monitoring configuration
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
```

### Common Commands

```bash
# Full application build
./scripts/build.sh

# Setup development environment
./scripts/setup-monitoring.sh

# Clean up containers
docker-compose -f infrastructure/docker/docker-compose.yml down

# View logs
docker-compose -f infrastructure/docker/docker-compose.yml logs -f
```

## Script Details

### build.sh

**Purpose**: Builds Docker images for backend and frontend services.

**Features**:
- Multi-stage builds for optimization
- Environment-specific configurations
- Image tagging and registry pushing
- Build validation and testing

**Usage**:
```bash
./scripts/build.sh [service] [environment]
```

**Examples**:
```bash
# Build all services
./scripts/build.sh

# Build only backend
./scripts/build.sh backend

# Build with specific environment
./scripts/build.sh all production
```

### setup-monitoring.sh

**Purpose**: Sets up the monitoring infrastructure for local development.

**Features**:
- Prometheus configuration
- Grafana dashboard setup
- Service discovery configuration
- Health check validation

**Usage**:
```bash
./scripts/setup-monitoring.sh
```

## Customization

### Adding New Scripts

1. Create script in `scripts/` directory
2. Make executable: `chmod +x scripts/your-script.sh`
3. Add to this README
4. Include proper error handling and logging

### Script Template

```bash
#!/bin/bash

# Script description
# Usage: ./scripts/script-name.sh [options]

set -e  # Exit on error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Functions
log_info() {
    echo "[INFO] $1"
}

log_error() {
    echo "[ERROR] $1" >&2
}

# Main execution
main() {
    log_info "Starting script execution"
    
    # Your script logic here
    
    log_info "Script completed successfully"
}

# Error handling
trap 'log_error "Script failed at line $LINENO"' ERR

# Run main function
main "$@"
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x scripts/*.sh
   ```

2. **Script Not Found**
   - Ensure you're in the project root
   - Use absolute paths: `./scripts/build.sh`

3. **Docker Issues**
   - Verify Docker is running
   - Check Docker Compose version
   - Validate docker-compose.yml syntax

### Debug Mode

Enable debug output:

```bash
# Bash debug mode
bash -x ./scripts/build.sh

# Verbose output
./scripts/build.sh --verbose
```

## Contributing

When adding new scripts:

1. Follow the established naming conventions
2. Include proper error handling
3. Add usage documentation
4. Test across different environments
5. Update this README
