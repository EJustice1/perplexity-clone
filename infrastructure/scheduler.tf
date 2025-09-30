# Cloud Scheduler configuration for invoking the dispatcher service on a fixed cadence

locals {
  dispatcher_default_path        = "/dispatcher/dispatch"
  dispatcher_scheduler_target_uri = var.scheduler_dispatcher_uri != "" ? var.scheduler_dispatcher_uri : "${google_cloud_run_v2_service.dispatcher.uri}${local.dispatcher_default_path}"
  dispatcher_scheduler_audience   = google_cloud_run_v2_service.dispatcher.uri
}

resource "google_cloud_scheduler_job" "dispatcher_weekly" {
  name        = "${var.app_name}-dispatcher-weekly"
  description = "Weekly trigger that invokes the dispatcher service to start batch processing."
  schedule    = var.scheduler_schedule
  time_zone   = var.scheduler_time_zone
  attempt_deadline = "300s"
  region      = var.region

  retry_config {
    retry_count          = 3
    max_retry_duration   = "0s"
    min_backoff_duration = "30s"
    max_backoff_duration = "300s"
    max_doublings        = 3
  }

  http_target {
    http_method = "POST"
    uri         = local.dispatcher_scheduler_target_uri

    headers = {
      "Content-Type"      = "application/json"
      "X-Cloud-Scheduler" = "${var.app_name}-weekly-dispatch"
    }

    body = base64encode(jsonencode({
      trigger_source = "cloud-scheduler"
      job_id         = "${var.app_name}-dispatcher-weekly"
    }))

    oidc_token {
      service_account_email = google_service_account.scheduler_sa.email
      audience              = local.dispatcher_scheduler_audience
    }
  }

  depends_on = [google_cloud_run_service_iam_member.dispatcher_scheduler_invoker]
}

