# Service Account for Cloud Run services
resource "google_service_account" "cloud_run_sa" {
  account_id   = "${var.app_name}-cloud-run-sa"
  display_name = "Service Account for ${var.app_name} Cloud Run services"
  description  = "Service account used by Cloud Run services to access GCP resources"
}

# IAM roles for the service account
resource "google_project_iam_member" "cloud_run_sa_roles" {
  for_each = toset([
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/run.invoker",
    "roles/artifactregistry.reader",
    "roles/datastore.user",
    "roles/cloudscheduler.jobRunner",
    "roles/redis.viewer",
    "roles/pubsub.editor"
  ])
  
  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# Allow the service account to access Artifact Registry
resource "google_artifact_registry_repository_iam_member" "repository_reader" {
  location   = google_artifact_registry_repository.app_repository.location
  repository = google_artifact_registry_repository.app_repository.name
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# Service Account for Cloud Scheduler invocations
resource "google_service_account" "scheduler_sa" {
  account_id   = "${var.app_name}-scheduler-sa"
  display_name = "Service Account for ${var.app_name} Cloud Scheduler"
  description  = "Invokes dispatcher Cloud Run service on schedule"
}

# Scheduler IAM to invoke dispatcher service
resource "google_cloud_run_service_iam_member" "dispatcher_scheduler_invoker" {
  location = google_cloud_run_v2_service.dispatcher.location
  service  = google_cloud_run_v2_service.dispatcher.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.scheduler_sa.email}"
}
