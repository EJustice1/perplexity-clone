# Local values for computed URLs - only use static URLs to avoid circular dependency
locals {
  frontend_urls = var.frontend_urls
}

# Backend Cloud Run Service
resource "google_cloud_run_v2_service" "backend" {
  name     = "${var.app_name}-backend"
  location = var.region

  template {
    containers {
      image = var.backend_image != "" ? var.backend_image : "${var.region}-docker.pkg.dev/${var.project_id}/${var.app_name}-repository/backend:latest"
      
      ports {
        container_port = 8000
      }

      resources {
        limits = {
          cpu    = "1000m"
          memory = "1Gi"
        }
      }

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }

      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }

      env {
        name  = "REGION"
        value = var.region
      }

      env {
        name  = "CORS_ORIGINS"
        value = join(",", concat(local.frontend_urls, [google_cloud_run_v2_service.frontend.uri]))
      }

    }

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }

    service_account = google_service_account.cloud_run_sa.email
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  labels = {
    environment = var.environment
    app         = var.app_name
    service     = "backend"
    managed-by  = "terraform"
    cost-center = "engineering"
    team        = "platform"
  }
}

# Frontend Cloud Run Service
resource "google_cloud_run_v2_service" "frontend" {
  name     = "${var.app_name}-frontend"
  location = var.region

  template {
    containers {
      image = var.frontend_image != "" ? var.frontend_image : "${var.region}-docker.pkg.dev/${var.project_id}/${var.app_name}-repository/frontend:latest"
      
      ports {
        container_port = 3000
      }

      resources {
        limits = {
          cpu    = "1000m"
          memory = "2Gi"
        }
      }

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }

      # PORT is automatically set by Cloud Run

      # NEXT_PUBLIC_API_URL is now set at build time via Docker build args
      # This ensures the frontend is built with the correct backend URL
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }

    service_account = google_service_account.cloud_run_sa.email
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  labels = {
    environment = var.environment
    app         = var.app_name
    service     = "frontend"
    managed-by  = "terraform"
    cost-center = "engineering"
    team        = "platform"
  }
}

# Allow unauthenticated access to frontend
resource "google_cloud_run_service_iam_member" "frontend_public" {
  location = google_cloud_run_v2_service.frontend.location
  service  = google_cloud_run_v2_service.frontend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Allow only the frontend service account to access the backend
resource "google_cloud_run_service_iam_member" "backend_frontend_access" {
  location = google_cloud_run_v2_service.backend.location
  service  = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}
