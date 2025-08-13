# Infrastructure as Code - Google Cloud Platform

This directory contains the Terraform configuration for deploying the Perplexity Clone application to Google Cloud Platform.

## Architecture Overview

The infrastructure creates:

- **Google Artifact Registry**: For storing Docker images
- **Google Secret Manager**: For managing application secrets
- **Cloud Run Services**: Backend and frontend services
- **Global Load Balancer**: With path-based routing (`/api/*` → backend, everything else → frontend)
- **SSL Certificates**: Managed HTTPS certificates
- **VPC Network**: Isolated network for the load balancer
- **Service Account**: With minimal required permissions

## Prerequisites

1. **Google Cloud SDK**: Install and authenticate with `gcloud auth login`
2. **Terraform**: Version 1.0 or higher
3. **GCP Project**: With billing enabled and required APIs enabled
4. **Docker Images**: Built and ready to deploy

## Required GCP APIs

Enable these APIs in your GCP project:

```bash
gcloud services enable \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  run.googleapis.com \
  compute.googleapis.com \
  cloudbuild.googleapis.com
```

## Quick Start

1. **Configure Variables**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your project details
   ```

2. **Deploy Infrastructure**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

## Manual Deployment

If you prefer manual deployment:

```bash
# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Apply configuration
terraform apply
```

## Configuration

### Required Variables

- `project_id`: Your GCP Project ID

### Optional Variables

- `region`: GCP region (default: us-central1)
- `zone`: GCP zone (default: us-central1-a)
- `environment`: Environment name (default: dev)
- `domain_name`: Custom domain (optional)
- `backend_image`: Custom backend image URI
- `frontend_image`: Custom frontend image URI

## Outputs

After successful deployment, Terraform will output:

- `load_balancer_ip`: Public IP address of the load balancer
- `frontend_url`: Direct URL to the frontend Cloud Run service
- `backend_url`: Direct URL to the backend Cloud Run service
- `artifact_registry_repository`: Repository name for Docker images

## Path-Based Routing

The load balancer routes traffic as follows:

- **`/api/*`** → Backend Cloud Run service
- **All other paths** → Frontend Cloud Run service

This allows the frontend to make API calls to `/api/v1/process-text` and have them automatically routed to the backend.

## Security

- **Service Account**: Minimal permissions principle
- **Public Access**: Services are publicly accessible (required for load balancer)
- **SSL**: HTTPS enforced with managed certificates
- **VPC**: Isolated network for load balancer components

## Cost Optimization

- **Cloud Run**: Scales to zero when not in use
- **Load Balancer**: Pay-per-use pricing
- **Artifact Registry**: Storage costs for Docker images
- **Secret Manager**: Minimal cost for secrets

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure your account has the necessary IAM roles
2. **API Not Enabled**: Enable required GCP APIs
3. **Billing Not Enabled**: Enable billing for your GCP project
4. **Image Pull Errors**: Ensure Docker images exist in Artifact Registry

### Debug Commands

```bash
# Check Terraform state
terraform show

# View logs
terraform logs

# Destroy infrastructure
terraform destroy
```

## Next Steps

After infrastructure deployment:

1. **Build and Push Docker Images** to Artifact Registry
2. **Update Cloud Run Services** with new image URIs
3. **Configure CI/CD Pipeline** for automated deployments
4. **Set up Monitoring** and alerting

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
