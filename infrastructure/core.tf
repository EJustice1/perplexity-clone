# Google Artifact Registry for Docker images
resource "google_artifact_registry_repository" "app_repository" {
  location      = var.region
  repository_id = "${var.app_name}-repository"
  description   = "Docker repository for ${var.app_name} application images"
  format        = "DOCKER"
  
  labels = {
    environment = var.environment
    app         = var.app_name
    managed-by  = "terraform"
    cost-center = "engineering"
    team        = "platform"
  }
}

# Google Secret Manager for application secrets
resource "google_secret_manager_secret" "app_secrets" {
  secret_id = "${var.app_name}-secrets"
  
  labels = {
    environment = var.environment
    app         = var.app_name
    managed-by  = "terraform"
    cost-center = "engineering"
    team        = "platform"
  }

  replication {
    auto {}
  }
}

# Create a placeholder secret value (will be updated later)
resource "google_secret_manager_secret_version" "app_secrets_version" {
  secret      = google_secret_manager_secret.app_secrets.id
  secret_data = "placeholder-secret-value"
}

# IAM for Secret Manager access
resource "google_secret_manager_secret_iam_member" "secret_access" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.app_secrets.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}
