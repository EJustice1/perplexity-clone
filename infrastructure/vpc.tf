# VPC and VPC Access Connector for Cloud Run to reach Memorystore

resource "google_vpc_access_connector" "cloud_run" {
  name          = "${var.app_name}-vpc-connector"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.8.0.0/28"

  depends_on = [google_project_service.required]
}

