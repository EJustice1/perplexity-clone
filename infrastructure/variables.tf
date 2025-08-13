variable "project_id" {
  description = "The ID of the GCP project where resources will be created"
  type        = string
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
  description = "List of frontend URLs for CORS configuration"
  type        = list(string)
  default     = [
    "http://localhost:3000",
    "https://perplexity-clone-frontend-233562799891.us-central1.run.app",
    "https://perplexity-clone-frontend-rg6a7wrdka-uc.a.run.app"
  ]
}
