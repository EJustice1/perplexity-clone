# GitHub Configuration

This directory contains GitHub-specific configuration files for CI/CD, testing, and automation.

## Test Configuration System

### Overview
The test configuration system eliminates hardcoded tests from the CI/CD pipeline by using external configuration files and dynamic test runners.

### Files
- **`test-config.yml`** - Configuration file defining all API endpoints, request bodies, and expected responses
- **`scripts/test-api.py`** - Python test runner that reads the configuration and executes tests
- **`scripts/requirements.txt`** - Python dependencies for the test runner

### How It Works

1. **Configuration-Driven**: All test parameters are defined in `test-config.yml`
2. **Dynamic Execution**: The Python test runner reads the configuration and executes tests accordingly
3. **Easy Maintenance**: Add new endpoints or modify existing ones by updating the config file
4. **No Hardcoding**: The CI/CD pipeline contains no hardcoded test values

### Adding New Tests

To add a new API endpoint test:

1. **Update `test-config.yml`**:
```yaml
api_endpoints:
  new_endpoint:
    path: /api/v1/new-endpoint
    method: POST
    auth_required: true
    request_body: '{"key":"value"}'
    expected_status: 200
    success_pattern: "expected response pattern"
    description: "Description of what this endpoint does"
```

2. **Add test method to `test-api.py`**:
```python
def test_new_endpoint(self) -> TestResult:
    """Test the new endpoint"""
    # Implementation here
    pass
```

3. **Update the test list in `run_all_tests()`**:
```python
tests = [
    self.test_health_endpoint,
    self.test_search_endpoint_auth,
    self.test_cors_functionality,
    self.test_error_handling,
    self.test_new_endpoint  # Add this line
]
```

### Benefits

- **Maintainable**: Tests are defined in configuration, not code
- **Flexible**: Easy to add/remove/modify tests without touching CI/CD
- **Readable**: Clear separation between test logic and test data
- **Reusable**: Test configuration can be used by other tools
- **Version Controlled**: Test changes are tracked in git

### Example Configuration

```yaml
api_endpoints:
  health:
    path: /health
    method: GET
    auth_required: false
    request_body: null
    expected_status: 200
    success_pattern: null
    description: "Health check endpoint"
    
  search:
    path: /api/v1/search
    method: POST
    auth_required: true
    request_body: '{"query":"test"}'
    expected_status: 200
    success_pattern: "You searched for:"
    description: "Search functionality endpoint"
```

### Running Tests Locally

```bash
# Install dependencies
pip install -r .github/scripts/requirements.txt

# Run tests
python .github/scripts/test-api.py "http://localhost:8000" "http://localhost:3000"
```

### CI/CD Integration

The CI/CD pipeline automatically:
1. Loads the test configuration
2. Installs test dependencies
3. Runs all configured tests
4. Reports results

No manual intervention required when adding new tests!
