# Memorystore (Redis) instance for topic change detection cache
resource "google_compute_global_address" "psa_range" {
  name          = "${var.app_name}-psa-range"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = var.psa_prefix_length
  network       = google_compute_network.vpc.id
}

resource "google_service_networking_connection" "psa_connection" {
  network                 = google_compute_network.vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.psa_range.name]
}

resource "google_redis_instance" "change_cache" {
  name           = "${var.app_name}-redis"
  project        = var.project_id
  region         = var.region
  tier           = var.redis_tier
  memory_size_gb = var.redis_memory_size_gb

  location_id  = var.redis_location != "" ? var.redis_location : null
  display_name = "${var.app_name} change cache"

  authorized_network      = google_compute_network.vpc.id
  connect_mode            = "PRIVATE_SERVICE_ACCESS"
  transit_encryption_mode = "DISABLED"

  labels = {
    environment = var.environment
    app         = var.app_name
    service     = "redis"
    managed-by  = "terraform"
  }

  depends_on = [
    google_service_networking_connection.psa_connection,
    google_project_service.required
  ]
}

