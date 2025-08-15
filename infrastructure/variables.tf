variable "project_id" {
  description = "The ID of the GCP project where resources will be created"
  type        = string
  
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.project_id))
    error_message = "Project ID must be 6-30 characters, lowercase letters, numbers, and hyphens only, starting with a letter."
  }
}

variable "region" {
  description = "The GCP region where resources will be created"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "The GCP zone for zonal resources"
  type        = string
  default     = "us-central1-a"
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "app_name" {
  description = "Application name used for resource naming"
  type        = string
  default     = "perplexity-clone"
}

variable "domain_name" {
  description = "Domain name for the application (optional)"
  type        = string
  default     = ""
}

variable "enable_ssl" {
  description = "Whether to enable SSL certificates"
  type        = bool
  default     = true
}

variable "backend_image" {
  description = "Backend Docker image URI"
  type        = string
  default     = ""
}

variable "frontend_image" {
  description = "Frontend Docker image URI"
  type        = string
  default     = ""
}

variable "frontend_urls" {
  description = "List of frontend URLs for CORS configuration (local development and production URLs)"
  type        = list(string)
  default     = [
    "http://localhost:3000",
    "https://localhost:3000",
    # Cloud Run new format - allow all us-central1.run.app domains
    "https://*.us-central1.run.app",
    # Legacy format for backward compatibility
    "https://*.perplexity-clone-468820.run.app",
    # New GCP Cloud Run format (random hash)
    "https://*.a.run.app"
  ]
}
