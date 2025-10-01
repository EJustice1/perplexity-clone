# Configuration for Perplexity Clone infrastructure deployment

# Required: Your GCP Project ID
project_id = "perplexity-clone-468820"

# Required: Application name for resource naming
app_name = "perplexity-clone"

# Celery configuration supplied via Terraform variables (populate with Redis endpoints)
celery_broker_url      = "redis://redis-hostname:6379/0"
celery_result_backend  = "redis://redis-hostname:6379/1"

# Optional: Override default region and zone
region = "us-central1"
zone   = "us-central1-a"

# Optional: Environment name
environment = "dev"

# Optional: Custom domain name (if you have one)
# domain_name = "yourdomain.com"

# Docker images (using Artifact Registry)
backend_image = "us-central1-docker.pkg.dev/perplexity-clone-468820/perplexity-clone-repository/backend:latest"
frontend_image = "us-central1-docker.pkg.dev/perplexity-clone-468820/perplexity-clone-repository/frontend:latest"

# Scheduler configuration
scheduler_dispatcher_uri = "https://perplexity-clone-dispatcher-rg6a7wrdka-uc.a.run.app/dispatcher/dispatch"

# Required: API Keys for functionality
# Set these via GitHub Secrets or environment variables
# serper_api_key = "your_api_key_here"
# google_ai_api_key = "your_google_ai_api_key_here"
