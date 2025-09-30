# VPC Network for the load balancer
resource "google_compute_network" "vpc" {
  name                    = "${var.app_name}-vpc"
  auto_create_subnetworks = false
}

# Subnet for the load balancer
resource "google_compute_subnetwork" "subnet" {
  name          = "${var.app_name}-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
}

# External IP address for the load balancer
resource "google_compute_global_address" "lb_ip" {
  name         = "${var.app_name}-lb-ip"
  address_type = "EXTERNAL"
}

# Health check for backend service
resource "google_compute_health_check" "backend_health" {
  name = "${var.app_name}-backend-health"

  http_health_check {
    port = 8000
    request_path = "/health"
  }

  timeout_sec        = 5
  check_interval_sec = 10
}

# Health check for frontend service
resource "google_compute_health_check" "frontend_health" {
  name = "${var.app_name}-frontend-health"

  http_health_check {
    port = 3000
    request_path = "/"
  }

  timeout_sec        = 5
  check_interval_sec = 10
}

# Backend service for the load balancer
resource "google_compute_backend_service" "backend" {
  name                    = "${var.app_name}-backend-lb"
  protocol                = "HTTP"
  port_name               = "http"
  timeout_sec             = 30
  load_balancing_scheme   = "EXTERNAL_MANAGED"

  backend {
    group = google_compute_region_network_endpoint_group.backend_neg.id
  }

  # No health checks for serverless backends
}

# Dispatcher backend service for the load balancer
resource "google_compute_backend_service" "dispatcher" {
  name                    = "${var.app_name}-dispatcher-lb"
  protocol                = "HTTP"
  port_name               = "http"
  timeout_sec             = 30
  load_balancing_scheme   = "EXTERNAL_MANAGED"

  backend {
    group = google_compute_region_network_endpoint_group.dispatcher_neg.id
  }
}

# Worker backend service for the load balancer
resource "google_compute_backend_service" "worker" {
  name                    = "${var.app_name}-worker-lb"
  protocol                = "HTTP"
  port_name               = "http"
  timeout_sec             = 30
  load_balancing_scheme   = "EXTERNAL_MANAGED"

  backend {
    group = google_compute_region_network_endpoint_group.worker_neg.id
  }
}

# Frontend backend service for the load balancer
resource "google_compute_backend_service" "frontend" {
  name                    = "${var.app_name}-frontend-lb"
  protocol                = "HTTP"
  port_name               = "http"
  timeout_sec             = 30
  load_balancing_scheme   = "EXTERNAL_MANAGED"

  backend {
    group = google_compute_region_network_endpoint_group.frontend_neg.id
  }
}

# Network endpoint group for backend
resource "google_compute_region_network_endpoint_group" "backend_neg" {
  name                  = "${var.app_name}-backend-neg"
  region               = var.region
  cloud_run {
    service = google_cloud_run_v2_service.backend.name
  }
}

# Network endpoint group for dispatcher
resource "google_compute_region_network_endpoint_group" "dispatcher_neg" {
  name    = "${var.app_name}-dispatcher-neg"
  region  = var.region
  cloud_run {
    service = google_cloud_run_v2_service.dispatcher.name
  }
}

# Network endpoint group for worker
resource "google_compute_region_network_endpoint_group" "worker_neg" {
  name    = "${var.app_name}-worker-neg"
  region  = var.region
  cloud_run {
    service = google_cloud_run_v2_service.worker.name
  }
}

# Network endpoint group for frontend
resource "google_compute_region_network_endpoint_group" "frontend_neg" {
  name                  = "${var.app_name}-frontend-neg"
  region               = var.region
  cloud_run {
    service = google_cloud_run_v2_service.frontend.name
  }
}

# URL map for path-based routing
resource "google_compute_url_map" "url_map" {
  name            = "${var.app_name}-url-map"
  default_service = google_compute_backend_service.frontend.id

  host_rule {
    hosts        = ["*"]
    path_matcher = "api-routing"
  }

  path_matcher {
    name            = "api-routing"
    default_service = google_compute_backend_service.frontend.id

    path_rule {
      paths   = ["/api/*"]
      service = google_compute_backend_service.backend.id
    }

    path_rule {
      paths   = ["/dispatcher/*"]
      service = google_compute_backend_service.dispatcher.id
    }

    path_rule {
      paths   = ["/worker/*"]
      service = google_compute_backend_service.worker.id
    }
  }
}

# HTTPS proxy (only when SSL is enabled)
resource "google_compute_target_https_proxy" "https_proxy" {
  count            = var.enable_ssl ? 1 : 0
  name             = "${var.app_name}-https-proxy"
  url_map          = google_compute_url_map.url_map.id
  ssl_certificates = [google_compute_managed_ssl_certificate.ssl_cert[0].id]
}

# SSL certificate (managed by Google)
resource "google_compute_managed_ssl_certificate" "ssl_cert" {
  count   = var.enable_ssl ? 1 : 0
  name    = "${var.app_name}-ssl-cert"
  
  managed {
    domains = var.domain_name != "" ? [var.domain_name] : ["${var.app_name}.run.app"]
  }
}

# Global forwarding rule for HTTPS (only when SSL is enabled)
resource "google_compute_global_forwarding_rule" "https_forwarding_rule" {
  count                  = var.enable_ssl ? 1 : 0
  name                   = "${var.app_name}-https-forwarding-rule"
  target                 = google_compute_target_https_proxy.https_proxy[0].id
  port_range             = "443"
  ip_address             = google_compute_global_address.lb_ip.address
  load_balancing_scheme  = "EXTERNAL_MANAGED"
}

# HTTP to HTTPS redirect (only when SSL is enabled)
resource "google_compute_url_map" "http_redirect" {
  count   = var.enable_ssl ? 1 : 0
  name    = "${var.app_name}-http-redirect"
  
  default_url_redirect {
    https_redirect = true
    strip_query    = false
  }
}

resource "google_compute_target_http_proxy" "http_proxy" {
  count   = var.enable_ssl ? 1 : 0
  name    = "${var.app_name}-http-proxy"
  url_map = google_compute_url_map.http_redirect[0].id
}

resource "google_compute_global_forwarding_rule" "http_forwarding_rule" {
  count                  = var.enable_ssl ? 1 : 0
  name                   = "${var.app_name}-http-forwarding-rule"
  target                 = google_compute_target_http_proxy.http_proxy[0].id
  port_range             = "80"
  ip_address             = google_compute_global_address.lb_ip.address
  load_balancing_scheme  = "EXTERNAL_MANAGED"
}
