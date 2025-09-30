# Cloud Scheduler Runbook

## Overview
- **Job Name:** `perplexity-clone-dispatcher-weekly`
- **Purpose:** Trigger the dispatcher Cloud Run service every Monday at 09:00 UTC to kick off weekly batch processing.
- **Invocation Path:** `POST https://<load-balancer-domain>/dispatcher/dispatch`
- **Authentication:** OIDC token issued to scheduler service account `perplexity-clone-scheduler-sa@perplexity-clone-468820.iam.gserviceaccount.com`.

## Verification Steps
- **Manual Run:**
  1. `gcloud scheduler jobs run perplexity-clone-dispatcher-weekly --location=us-central1`
  2. Confirm Cloud Run log entry `Dispatcher trigger received` with status 204.
- **Schedule Check:**
  - `gcloud scheduler jobs describe perplexity-clone-dispatcher-weekly --location=us-central1`
  - Ensure schedule `0 9 * * MON` and time zone `Etc/UTC`.

## Monitoring & Alerting
- **Log Metrics:**
  - `perplexity-clone-dispatcher-scheduler-invocations`
  - `perplexity-clone-dispatcher-scheduler-failures`
- **Alert Recommendation:** Create alert if failures > 0 over 1 hour window; notify ops email.

## Common Issues
- **403 Responses:** Verify IAM binding `roles/run.invoker` for scheduler service account.
- **Missing Logs:** Ensure dispatcher container is deployed and logging driver active.
- **Schedule Drift:** Update Terraform variables `scheduler_schedule` or `scheduler_time_zone` and reapply.

## Change Log
- **2025-09-30:** Stage 3 implementation – initial job deployment, logging metrics, and documentation.
