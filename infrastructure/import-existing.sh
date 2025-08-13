#!/bin/bash

# Script to import existing GCP resources into Terraform state
# Run this from the infrastructure directory

set -e

echo "🔄 Importing existing GCP resources into Terraform state..."

# Set variables
PROJECT_ID="perplexity-clone-468820"
REGION="us-central1"

echo "🧹 Cleaning up any inconsistent Terraform state..."

# Remove resources that might be in an inconsistent state
terraform state rm google_artifact_registry_repository.app_repository 2>/dev/null || true
terraform state rm google_secret_manager_secret.app_secrets 2>/dev/null || true
terraform state rm google_compute_network.vpc 2>/dev/null || true
terraform state rm google_compute_global_address.lb_ip 2>/dev/null || true
terraform state rm google_compute_health_check.backend_health 2>/dev/null || true
terraform state rm google_compute_health_check.frontend_health 2>/dev/null || true
terraform state rm 'google_compute_managed_ssl_certificate.ssl_cert[0]' 2>/dev/null || true
terraform state rm 'google_compute_url_map.http_redirect[0]' 2>/dev/null || true
terraform state rm google_service_account.cloud_run_sa 2>/dev/null || true

echo "📋 Importing Artifact Registry repository..."
terraform import google_artifact_registry_repository.app_repository \
  "projects/${PROJECT_ID}/locations/${REGION}/repositories/perplexity-clone-repository"

echo "📋 Importing Secret Manager secret..."
terraform import google_secret_manager_secret.app_secrets \
  "projects/${PROJECT_ID}/secrets/perplexity-clone-secrets"

echo "📋 Importing VPC network..."
terraform import google_compute_network.vpc \
  "projects/${PROJECT_ID}/global/networks/perplexity-clone-vpc"

echo "📋 Importing global IP address..."
terraform import google_compute_global_address.lb_ip \
  "projects/${PROJECT_ID}/global/addresses/perplexity-clone-lb-ip"

echo "📋 Importing backend health check..."
terraform import google_compute_health_check.backend_health \
  "projects/${PROJECT_ID}/global/healthChecks/perplexity-clone-backend-health"

echo "📋 Importing frontend health check..."
terraform import google_compute_health_check.frontend_health \
  "projects/${PROJECT_ID}/global/healthChecks/perplexity-clone-frontend-health"

echo "📋 Importing SSL certificate..."
terraform import 'google_compute_managed_ssl_certificate.ssl_cert[0]' \
  "projects/${PROJECT_ID}/global/sslCertificates/perplexity-clone-ssl-cert"

echo "📋 Importing HTTP redirect URL map..."
terraform import 'google_compute_url_map.http_redirect[0]' \
  "projects/${PROJECT_ID}/global/urlMaps/perplexity-clone-http-redirect"

echo "📋 Importing service account..."
terraform import google_service_account.cloud_run_sa \
  "projects/${PROJECT_ID}/serviceAccounts/perplexity-clone-cloud-run-sa@${PROJECT_ID}.iam.gserviceaccount.com"

echo "✅ Import completed! Now run: terraform plan"
echo "📝 Note: You may need to manually import Cloud Run services if they exist"
