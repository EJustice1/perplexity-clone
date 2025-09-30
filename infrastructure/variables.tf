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
    # Specific Cloud Run URLs for CORS (wildcards don't work with preflight)
    "https://perplexity-clone-frontend-rg6a7wrdka-uc.a.run.app",
    "https://perplexity-clone-backend-rg6a7wrdka-uc.a.run.app",
    "https://perplexity-clone-frontend-233562799891.us-central1.run.app/",
    "https://perplexity-clone-backend-233562799891.us-central1.run.app/"
  ]
}

variable "firestore_location" {
  description = "App Engine location (locking value once created)"
  type        = string
  default     = "us-central"
}

variable "firestore_database_location" {
  description = "Native Firestore database location (e.g. nam5, us-central1)"
  type        = string
  default     = ""
}

variable "firestore_collection" {
  description = "Firestore collection name for subscriptions"
  type        = string
  default     = "topic_subscriptions"
}

variable "backend_service_url" {
  description = "Backend Cloud Run service URL"
  type        = string
  default     = "https://perplexity-clone-backend-rg6a7wrdka-uc.a.run.app"
}

variable "serper_api_key" {
  description = "Serper.dev API key for web search functionality"
  type        = string
  sensitive   = true
  default     = ""
}

variable "google_ai_api_key" {
  description = "Google AI API key for Gemini LLM functionality"
  type        = string
  sensitive   = true
  default     = ""
}
