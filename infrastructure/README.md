# Infrastructure as Code

This directory contains the Terraform configuration for deploying the Interactive Search Engine infrastructure on Google Cloud Platform.

## Recent Changes

### Remote State Management
- **Before**: Local Terraform state files (not suitable for team collaboration)
- **After**: Remote state stored in Google Cloud Storage with versioning
- **Benefits**: Team collaboration, state locking, backup and recovery

### Container Registry
- **Before**: Google Container Registry (GCR) - deprecated
- **After**: Google Artifact Registry - modern, recommended solution
- **Benefits**: Better security, performance, and integration

### Security Improvements
- **Before**: Backend API publicly accessible
- **After**: Backend API restricted to frontend service only
- **Benefits**: Improved security, reduced attack surface

## Prerequisites

1. **Google Cloud CLI**: Install and authenticate with `gcloud auth login`
2. **Terraform**: Version 1.0 or higher
3. **Project Access**: Ensure you have access to the GCP project

## Quick Start

### First Time Setup

1. **Configure Variables**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your project details
   ```

2. **Migrate to Remote State** (if coming from local state):
   ```bash
   ./migrate-to-remote-state.sh
   ```

3. **Deploy Infrastructure**:
   ```bash
   ./deploy.sh
   ```

### Normal Deployment

```bash
terraform init
terraform plan
terraform apply
```

## Architecture

### Components

- **Google Cloud Run**: Hosts frontend and backend services
- **Google Artifact Registry**: Stores Docker images
- **Google Cloud Load Balancer**: Routes traffic and provides SSL termination
- **Google Secret Manager**: Manages application secrets
- **Google Cloud Storage**: Stores Terraform state remotely

### Network Architecture

```
Internet → Load Balancer → Frontend (Cloud Run)
                    ↓
                Backend (Cloud Run) ← Service Account Auth
```

## State Management

### Remote State Configuration

The Terraform state is stored remotely in Google Cloud Storage:

```hcl
terraform {
  backend "gcs" {
    bucket = "perplexity-clone-terraform-state-{project-id}"
    prefix = "terraform/state"
  }
}
```

### State Migration

If you're migrating from local state to remote state:

1. Run the migration script: `./migrate-to-remote-state.sh`
2. The script will:
   - Create the GCS bucket
   - Enable versioning
   - Reconfigure Terraform to use remote state
   - Preserve your existing infrastructure

## Security

### Service Account Permissions

The Cloud Run services use a dedicated service account with minimal required permissions:
- `roles/logging.logWriter` - Write application logs
- `roles/monitoring.metricWriter` - Write metrics
- `roles/run.invoker` - Invoke Cloud Run services
- `roles/artifactregistry.reader` - Read Docker images

### Access Control

- **Frontend**: Publicly accessible
- **Backend**: Accessible only to frontend service account
- **Artifact Registry**: Private repository with service account access
- **Terraform State**: Private GCS bucket with versioning

## Troubleshooting

### Common Issues

1. **State Lock Errors**: Wait for other operations to complete
2. **Permission Errors**: Verify service account has required roles
3. **Image Pull Errors**: Check Artifact Registry permissions
4. **Health Check Failures**: Verify health endpoints are accessible

### Debugging

1. **Check Terraform State**:
   ```bash
   terraform state list
   terraform show
   ```

2. **Check Service Logs**:
   ```bash
   gcloud logging read "resource.type=cloud_run_revision"
   ```

3. **Verify Permissions**:
   ```bash
   gcloud projects get-iam-policy $PROJECT_ID
   ```

## Maintenance

### Regular Tasks

1. **Update Dependencies**: Run `terraform init -upgrade`
2. **Review Changes**: Always run `terraform plan` before applying
3. **Backup State**: State is automatically versioned in GCS
4. **Clean Up**: Remove unused resources with `terraform destroy`

### Cost Optimization

- Use `min_instance_count = 0` for non-critical services
- Monitor resource usage in Google Cloud Console
- Set up billing alerts for cost thresholds

## Future Enhancements

- **Multi-Environment**: Separate state files for dev/staging/prod
- **State Locking**: Implement proper state locking with Cloud Storage
- **Automated Backups**: Regular state backup and recovery testing
- **Monitoring**: Integration with Google Cloud Operations

## File Structure

```
infrastructure/
├── terraform.tf          # Main Terraform configuration
├── variables.tf          # Input variables
├── core.tf              # Core resources (Artifact Registry, Secret Manager)
├── service-accounts.tf  # Service account and IAM
├── cloud-run.tf         # Cloud Run services
├── load-balancer.tf     # Load balancer and networking
├── outputs.tf           # Output values
├── terraform.tfvars.example # Example configuration
├── deploy.sh            # Deployment script
└── README.md            # This file
```

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review Terraform documentation
3. Check GCP Cloud Console for resource status
4. Review Cloud Run logs for application issues
