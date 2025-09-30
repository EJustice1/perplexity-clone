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
        value = join(",", concat(local.frontend_urls, [
          "https://${google_compute_global_address.lb_ip.address}",
          "http://${google_compute_global_address.lb_ip.address}"
        ]))
      }

      env {
        name  = "FRONTEND_URL"
        value = "https://${var.app_name}-frontend-${var.project_id}.${var.region}.run.app"
      }

      env {
        name  = "LOAD_BALANCER_URL"
        value = var.enable_ssl ? "https://${google_compute_global_address.lb_ip.address}" : "http://${google_compute_global_address.lb_ip.address}"
      }

      env {
        name  = "SERPER_API_KEY"
        value = var.serper_api_key
      }

      env {
        name  = "GOOGLE_AI_API_KEY"
        value = var.google_ai_api_key
      }

      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }

      env {
        name  = "FIRESTORE_COLLECTION"
        value = var.firestore_collection
      }

    }

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }

    vpc_access {
      connector = google_vpc_access_connector.cloud_run.id
      egress    = "PRIVATE_RANGES_ONLY"
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

      env {
        name  = "BACKEND_SERVICE_URL"
        value = google_cloud_run_v2_service.backend.uri
      }

      env {
        name  = "NEXT_PUBLIC_LOAD_BALANCER_URL"
        value = var.enable_ssl ? "https://${google_compute_global_address.lb_ip.address}" : "http://${google_compute_global_address.lb_ip.address}"
      }

    }

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }

    vpc_access {
      connector = google_vpc_access_connector.cloud_run.id
      egress    = "PRIVATE_RANGES_ONLY"
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

# Allow unauthenticated access to backend for browser requests (CORS)
# Security is maintained through CORS origin validation in the application
resource "google_cloud_run_service_iam_member" "backend_public_access" {
  location = google_cloud_run_v2_service.backend.location
  service  = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}


# Dispatcher Cloud Run Service
resource "google_cloud_run_v2_service" "dispatcher" {
  name     = "${var.app_name}-dispatcher"
  location = var.region

  template {
    containers {
      image = var.dispatcher_image != "" ? var.dispatcher_image : "${var.region}-docker.pkg.dev/${var.project_id}/${var.app_name}-repository/dispatcher:latest"

      ports {
        container_port = 8000
      }

      resources {
        limits = {
          cpu    = "1000m"
          memory = "512Mi"
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
        name  = "FIRESTORE_COLLECTION"
        value = var.firestore_collection
      }

      env {
        name  = "MEMORYSTORE_HOST"
        value = google_redis_instance.change_cache.host
      }

      env {
        name  = "MEMORYSTORE_PORT"
        value = tostring(google_redis_instance.change_cache.port)
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 5
    }

    vpc_access {
      connector = google_vpc_access_connector.cloud_run.id
      egress    = "PRIVATE_RANGES_ONLY"
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
    service     = "dispatcher"
    managed-by  = "terraform"
  }
}

# Worker Cloud Run Service
resource "google_cloud_run_v2_service" "worker" {
  name     = "${var.app_name}-worker"
  location = var.region

  template {
    containers {
      image = var.worker_image != "" ? var.worker_image : "${var.region}-docker.pkg.dev/${var.project_id}/${var.app_name}-repository/worker:latest"

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
        name  = "FIRESTORE_COLLECTION"
        value = var.firestore_collection
      }

      env {
        name  = "MEMORYSTORE_HOST"
        value = google_redis_instance.change_cache.host
      }

      env {
        name  = "MEMORYSTORE_PORT"
        value = tostring(google_redis_instance.change_cache.port)
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 5
    }

    vpc_access {
      connector = google_vpc_access_connector.cloud_run.id
      egress    = "PRIVATE_RANGES_ONLY"
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
    service     = "worker"
    managed-by  = "terraform"
  }
}

# Allow internal invocations between services
