#!/bin/bash

# Terraform deployment script for Perplexity Clone infrastructure
# This script automates the deployment process

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

print_status "Starting Terraform deployment..."

# Initialize Terraform
print_status "Initializing Terraform..."
terraform init

# Plan the deployment
print_status "Planning deployment..."
terraform plan -out=tfplan

# Ask for confirmation
echo
read -p "Do you want to apply this plan? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Applying Terraform plan..."
    terraform apply tfplan
    
    print_status "Deployment completed successfully!"
    print_status "Load Balancer IP: $(terraform output -raw load_balancer_ip)"
    print_status "Frontend URL: $(terraform output -raw frontend_url)"
    print_status "Backend URL: $(terraform output -raw backend_url)"
    
    # Clean up plan file
    rm tfplan
    
    print_status "You can now access your application at: http://$(terraform output -raw load_balinator_ip)"
else
    print_warning "Deployment cancelled."
    rm tfplan
    exit 0
fi
