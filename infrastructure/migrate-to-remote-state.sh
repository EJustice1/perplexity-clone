#!/bin/bash

# Migration script to move from local Terraform state to remote GCS state
# This script should be run after the GCS bucket is created

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "Starting migration to remote state..."

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    print_error "terraform.tfvars file not found!"
    print_status "Please copy terraform.tfvars.example to terraform.tfvars and configure your values."
    exit 1
fi

# Check if gcloud is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    print_error "You are not authenticated with gcloud!"
    print_status "Please run: gcloud auth login"
    exit 1
fi

# Check if gcloud config has a project set
if ! gcloud config get-value project 2>/dev/null | grep -q .; then
    print_error "No GCP project is set in gcloud config!"
    print_status "Please run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

PROJECT_ID=$(gcloud config get-value project)
REGION=$(grep '^region' terraform.tfvars | cut -d'"' -f2 || echo "us-central1")
APP_NAME=$(grep '^app_name' terraform.tfvars | cut -d'"' -f2 || echo "perplexity-clone")

BUCKET_NAME="${APP_NAME}-terraform-state-${PROJECT_ID}"

print_status "Project ID: $PROJECT_ID"
print_status "Region: $REGION"
print_status "App Name: $APP_NAME"
print_status "State Bucket: $BUCKET_NAME"

# Create the GCS bucket if it doesn't exist
print_status "Creating GCS bucket for Terraform state..."
gsutil mb -p "$PROJECT_ID" -c STANDARD -l "$REGION" "gs://$BUCKET_NAME" || print_warning "Bucket may already exist"

# Enable versioning on the bucket
print_status "Enabling versioning on state bucket..."
gsutil versioning set on "gs://$BUCKET_NAME"

# Initialize Terraform with remote backend
print_status "Initializing Terraform with remote backend..."
terraform init -reconfigure

print_status "Migration completed successfully!"
print_status "Your Terraform state is now stored remotely in: gs://$BUCKET_NAME"
print_status "You can now run 'terraform plan' and 'terraform apply' normally."
print_status "Remember to commit and push your changes to share the remote state with your team."
