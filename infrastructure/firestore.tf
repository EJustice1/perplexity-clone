resource "google_project_service" "firestore" {
  project = var.project_id
  service = "firestore.googleapis.com"
}

resource "google_project_service" "appengine" {
  project = var.project_id
  service = "appengine.googleapis.com"
}

resource "google_app_engine_application" "default" {
  project       = var.project_id
  location_id   = var.firestore_location
  database_type = "CLOUD_FIRESTORE"

  depends_on = [google_project_service.appengine]
}

resource "google_firestore_database" "default" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.firestore_location
  type        = "FIRESTORE_NATIVE"

  depends_on = [
    google_project_service.firestore,
    google_app_engine_application.default,
  ]
}

