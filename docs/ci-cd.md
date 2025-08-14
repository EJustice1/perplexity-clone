# CI/CD Pipeline Documentation

This document describes the comprehensive CI/CD pipeline implemented for the Interactive Search Engine project using GitHub Actions.

## Overview

The CI/CD pipeline automates the entire software delivery process from code commit to production deployment, including:

- **Continuous Integration**: Automated testing, linting, and code quality checks
- **Continuous Deployment**: Automated building, testing, and deployment to Google Cloud Platform
- **Security Scanning**: Automated vulnerability detection and dependency scanning
- **Maintenance**: Automated cleanup and dependency management

## Configuration

### Environment Variables

The pipeline uses GitHub repository variables for configuration:

- `PROJECT_ID`: Google Cloud Project ID (defaults to perplexity-clone-468820)
- `REGION`: Google Cloud region (defaults to us-central1)

These can be configured in your repository's Settings → Secrets and variables → Actions → Variables tab.

### Container Registry

The pipeline uses **Google Artifact Registry** instead of the legacy Google Container Registry (GCR):
- Repository: `{region}-docker.pkg.dev/{project-id}/{app-name}-repository`
- Images: `{region}-docker.pkg.dev/{project-id}/{app-name}-repository/{service}:{tag}`

## Workflow Files

### 1. Main CI/CD Pipeline (`ci-cd.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` branch
- Manual workflow dispatch

**Jobs:**
1. **Backend CI/CD**: Build, test, and deploy backend service
2. **Frontend CI/CD**: Build, test, and deploy frontend service
3. **Infrastructure**: Deploy infrastructure using Terraform
4. **Verification**: Post-deployment health checks and verification

### 2. Pull Request Validation (`pr-validation.yml`)

**Triggers:** Pull requests to `main` or `develop` branches

**Jobs:**
1. **Backend Validation**: Code quality, linting, type checking, and tests
2. **Frontend Validation**: Linting, type checking, tests, and build verification
3. **Security Scan**: Vulnerability scanning with Trivy
4. **Dependency Check**: Security vulnerability checks with Snyk

### 3. Maintenance & Security (`maintenance.yml`)

**Triggers:**
- Daily at 2 AM UTC (automated)
- Manual workflow dispatch

**Jobs:**
1. **Security Scan**: Automated security scanning
2. **Dependency Update**: Check for available dependency updates
3. **Cleanup**: Remove old Docker images (older than 30 days)

## Prerequisites

### GitHub Secrets

The following secrets must be configured in your GitHub repository:

```bash
# Google Cloud Service Account Key (base64 encoded)
GCP_SA_KEY=<base64-encoded-service-account-key>

# Snyk API Token (optional, for dependency scanning)
SNYK_TOKEN=<your-snyk-token>
```

### Google Cloud Setup

1. **Service Account**: Create a service account with the following roles:
   - `Cloud Run Admin`
   - `Storage Admin` (for Container Registry)
   - `Service Account User`
   - `Terraform Admin` (if using Terraform)

2. **Enable APIs**:
   - Cloud Run API
   - Container Registry API
   - Cloud Build API

3. **Generate Service Account Key**:
   ```bash
   gcloud iam service-accounts create github-actions \
     --display-name="GitHub Actions Service Account"
   
   gcloud projects add-iam-policy-binding $PROJECT_ID \
     --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/run.admin"
   
   gcloud iam service-accounts keys create key.json \
     --iam-account=github-actions@$PROJECT_ID.iam.gserviceaccount.com
   
   # Base64 encode for GitHub secret
   base64 -i key.json
   ```

## Pipeline Stages

### 1. Code Quality & Testing

**Backend:**
- Python dependency installation
- Code formatting with Black
- Linting with Flake8
- Type checking with MyPy
- Unit and integration tests with pytest
- Code coverage reporting

**Frontend:**
- Node.js dependency installation
- ESLint code quality checks
- TypeScript type checking
- Unit tests (if configured)
- Build verification

### 2. Security Scanning

- **Trivy**: Container and filesystem vulnerability scanning
- **Snyk**: Dependency vulnerability scanning
- **GitHub Security**: Integration with GitHub Security tab

### 3. Building & Packaging

- **Multi-platform Docker builds** (linux/amd64)
- **Layer caching** for faster builds
- **Image tagging** with commit SHA and latest
- **Push to Google Container Registry**

### 4. Deployment

- **Backend**: Deploy to Cloud Run with environment variables
- **Frontend**: Deploy to Cloud Run with backend URL configuration
- **Infrastructure**: Terraform deployment with new image references
- **Verification**: Health checks and accessibility tests

## Environment Management

### Environment Variables

The pipeline supports multiple environments:

- **dev**: Development environment (default)
- **staging**: Staging environment
- **prod**: Production environment

### Environment-Specific Configuration

```bash
# Manual deployment to specific environment
gh workflow run ci-cd.yml -f environment=staging

# Environment variables are automatically set
ENVIRONMENT=staging
CORS_ORIGINS=http://localhost:3000,https://staging-frontend.example.com
```

## Monitoring & Observability

### Deployment Summary

After each deployment, the pipeline creates a comprehensive summary including:
- Service URLs
- Environment information
- Commit SHA
- Deployment status

### Health Checks

The verification job performs:
- Backend health endpoint testing
- Frontend accessibility testing
- Service readiness verification

## Troubleshooting

### Common Issues

1. **Service Account Permissions**:
   ```bash
   # Verify service account has required roles
   gcloud projects get-iam-policy $PROJECT_ID \
     --flatten="bindings[].members" \
     --filter="bindings.members:github-actions@$PROJECT_ID.iam.gserviceaccount.com"
   ```

2. **Image Build Failures**:
   - Check Dockerfile syntax
   - Verify build context
   - Check for missing dependencies
   - Verify Artifact Registry permissions

3. **Deployment Failures**:
   - Verify service account permissions
   - Check Cloud Run quotas
   - Review deployment logs

### Debugging

1. **Enable Debug Logging**:
   ```yaml
   env:
     ACTIONS_STEP_DEBUG: true
   ```

2. **Manual Verification**:
   ```bash
   # Test backend health
   curl https://your-backend-url/health
   
   # Test frontend
   curl https://your-frontend-url/
   ```

## Best Practices

### Code Quality

1. **Pre-commit Hooks**: Use pre-commit hooks for local validation
2. **Branch Protection**: Require PR validation before merging
3. **Code Review**: Mandatory code review for all changes

### Security

1. **Regular Scans**: Daily automated security scanning
2. **Dependency Updates**: Regular dependency vulnerability checks
3. **Image Cleanup**: Automatic cleanup of old images

### Deployment

1. **Rollback Strategy**: Keep previous image versions for quick rollback
2. **Health Checks**: Comprehensive post-deployment verification
3. **Environment Isolation**: Separate environments for dev/staging/prod

## Future Enhancements

### Planned Features

1. **Blue-Green Deployment**: Zero-downtime deployment strategy
2. **Canary Releases**: Gradual rollout with monitoring
3. **Performance Testing**: Automated performance regression testing
4. **Chaos Engineering**: Automated failure testing

### Integration Opportunities

1. **Slack Notifications**: Deployment status notifications
2. **Jira Integration**: Automatic ticket updates
3. **Datadog Integration**: Deployment metrics and monitoring
4. **Feature Flags**: Dynamic feature toggling

## Support

For issues or questions about the CI/CD pipeline:

1. Check the GitHub Actions logs for detailed error information
2. Review the deployment verification results
3. Consult the troubleshooting section above
4. Create an issue in the repository with relevant details
