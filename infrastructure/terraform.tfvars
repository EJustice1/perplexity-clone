# Configuration for Perplexity Clone infrastructure deployment

# Required: Your GCP Project ID
project_id = "perplexity-clone-468820"

# Optional: Override default region and zone
region = "us-central1"
zone   = "us-central1-a"

# Optional: Environment name
environment = "dev"

# Optional: Custom domain name (if you have one)
# domain_name = "yourdomain.com"

# Docker images (using GCR instead of Artifact Registry)
backend_image = "gcr.io/perplexity-clone-468820/perplexity-clone-backend:latest"
frontend_image = "gcr.io/perplexity-clone-468820/perplexity-clone-frontend:latest"
