# Cloud Scheduler Runbook

## Overview
- **Job Name:** `perplexity-clone-dispatcher-weekly`
- **Purpose:** Trigger the dispatcher Cloud Run service every Monday at 09:00 UTC to kick off weekly batch processing.
- **Invocation Path:** `POST https://<load-balancer-domain>/dispatcher/dispatch`
- **Authentication:** OIDC token issued to scheduler service account `perplexity-clone-scheduler-sa@perplexity-clone-468820.iam.gserviceaccount.com`.

## Configuration
- Scheduler job: `perplexity-clone-dispatcher-weekly`
- Target URI: `/dispatcher/dispatch`
- Authentication: OIDC via scheduler service account
- SMTP secrets: stored in backend `.env` and GitHub repository secrets (Stage 5 email dispatch)
- Celery broker/backend URLs supplied via `celery_broker_url` / `celery_result_backend` Terraform variables (populated from `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` GitHub secrets); worker Cloud Run service runs Celery worker process.

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

## Local Test Script
- Use `python scripts/run_local_email_test.py --email foo@example.com --topic weekly-news` to enqueue a test task.
- Script ensures Docker Redis (`local-redis`) runs and pushes task via Celery.
- Requires `.env` with local Redis URLs and Firestore credentials accessible.
