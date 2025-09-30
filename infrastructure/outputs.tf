output "load_balancer_ip" {
  description = "IP address of the load balancer"
  value       = google_compute_global_address.lb_ip.address
}

output "frontend_url" {
  description = "URL of the frontend Cloud Run service"
  value       = google_cloud_run_v2_service.frontend.uri
}

output "backend_url" {
  description = "URL of the backend Cloud Run service"
  value       = google_cloud_run_v2_service.backend.uri
}

output "artifact_registry_repository" {
  description = "Artifact Registry repository for Docker images"
  value       = google_artifact_registry_repository.app_repository.name
}

output "service_account_email" {
  description = "Email of the service account used by Cloud Run services"
  value       = google_service_account.cloud_run_sa.email
}

output "scheduler_service_account_email" {
  description = "Email of the service account used by Cloud Scheduler"
  value       = google_service_account.scheduler_sa.email
}

output "dispatcher_scheduler_job_name" {
  description = "Name of the Cloud Scheduler job that triggers the dispatcher"
  value       = google_cloud_scheduler_job.dispatcher_weekly.name
}

output "project_id" {
  description = "GCP Project ID"
  value       = var.project_id
}

output "region" {
  description = "GCP Region where resources are deployed"
  value       = var.region
}

output "vpc_network" {
  description = "VPC network created for the load balancer"
  value       = google_compute_network.vpc.name
}
