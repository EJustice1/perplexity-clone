### **Implementation Plan: Cost-Minimal, Simple Weekly Subscription Service**

**Objective:**  
Provide a no-frills, low-cost weekly update system using Firestore for subscriptions, Memorystore Redis, Cloud Scheduler, Cloud Run, Celery, and basic SMTP email. Security and IAM roles can be added later.

***

### **Stage 1: Baseline Infrastructure Provisioning**

**Goal:**  
Establish all cloud resources required for the weekly subscription system using Terraform and GitHub Actions automation.

**Steps:**  
1. Configure Terraform backend and variables for the project.  
2. Provision shared services:
   - Google Artifact Registry for container images.  
   - Google Secret Manager for configuration secrets.  
   - Google Cloud Storage bucket for Terraform state (with versioning).  
   - Service accounts and IAM bindings for Cloud Run and automation.  
3. Deploy runtime infrastructure:
   - Cloud Run services for frontend, backend, dispatcher, and worker containers (min instances = 0, bounded max).  
   - External HTTPS load balancer with managed SSL and path routing.  
   - Cloud Firestore in Native mode for subscription storage.  
   - Cloud Memorystore (Redis) single-node instance for change detection cache.  
   - Cloud Scheduler weekly trigger targeting the dispatcher endpoint (Monday 9 AM).  
   - Pub/Sub topics or Cloud Tasks queues if needed for Celery interoperability (placeholders if implementation deferred).  
4. Update GitHub Actions workflows to build & deploy all services and run Terraform apply.  
5. Document infrastructure variables, outputs, and operational runbooks in `/docs`.

**Outcome:**  
All managed infrastructure is deployed and automated, ready for subsequent application logic stages.

***

### **Stage 2: Subscription Capture & Storage**

**Goal:**  
Collect and persist user `email`+`topic` subscriptions in Cloud Firestore.

**Steps:**  
1. Expose a web form endpoint that accepts `email` and `topic`.  
2. Validate: non-empty topic, well-formed email.  
3. Insert a Firestore document per subscription with fields:
   - `subscription_id` (UUID)  
   - `email`  
   - `topic`  
   - `created_at` (timestamp)  
   - `is_active` (true)  
   - `last_sent` (null)  

**Outcome:**  
All subscriptions are stored as individual, queryable documents with minimal overhead.

***

### **Stage 3: Single Fixed-Time Trigger**

**Goal:**  
Schedule one weekly job to start batch processing, avoiding always-on servers.

**Steps:**  
1. Confirm the Cloud Scheduler job created in Stage 1 successfully invokes the dispatcher endpoint every Monday at 9 AM.  
2. Surface monitoring/logging for trigger invocations.  

**Outcome:**  
A single managed schedule ensures predictable, low-cost invocation.

***

### **Stage 4: Batch Dispatcher on Cloud Run**

**Goal:**  
Retrieve all active subscriptions, group by topic, and enqueue processing tasks.

**Steps:**  
1. Cloud Run handler reads all Firestore subscriptions with `is_active = true`.  
2. Group subscriptions by identical `topic`.  
3. For each topic group, enqueue a Celery task (`process-topic`) with the topic and subscriber emails.  

**Outcome:**  
One Celery task per unique topic, minimizing redundant work and queue messages.

***

### **Stage 5: Fixed-Content Email Dispatch**

**Goal:**  
Deliver a simple weekly test email to every active subscriber.

**Steps:**  
1. Reuse the dispatcher batches to collect topic -> subscriber lists.  
2. Celery worker (or placeholder) schedules a `send-email` task per subscriber with fixed body text.  
3. Use a basic SMTP provider (e.g., Gmail sandbox) for delivery.  
4. Update Firestore `last_sent` timestamp after each email.  

**Outcome:**  
End-to-end email path validated with predictable content prior to dynamic summaries.

***

### **Stage 6: Answer Generation & Source Review**

**Goal:**  
Produce a synthesized weekly answer per topic with hooks for future source review and freshness checks.

**Steps:**  
1. Extend dispatcher batching to invoke an `generate-answer` task per topic.  
2. Use LangChain pipeline to gather sources and craft an answer, but skip change detection.  
3. Structure the result payload to include raw sources, answer text, and metadata for later freshness filtering.  
4. Store generated answers in Firestore or Redis for email usage.  

**Outcome:**  
Topics receive AI-generated summaries ready for manual or automated review, setting the stage for future delta checks.

***

### **Stage 7: New Information Detection**

**Goal:**  
Introduce Redis-backed change detection to compare this week’s answer and sources against previous runs.

**Steps:**  
1. Persist per-topic baselines (source hashes, answer digest, timestamp) in Memorystore Redis.  
2. Compare current LangChain outputs to baselines to flag new or changed information.  
3. Update baselines only when meaningful changes detected.  
4. Feed results into Stage 5 email flow to suppress unchanged topics.  

**Outcome:**  
Only fresh insights trigger email dispatches, minimizing noise and compute usage.

***

### **Stage 8: Minimal Configuration & Cost Control**

**Goal:**  
Keep infrastructure simple, serverless, and cost-minimal.

**Steps:**  
1. **Cloud Run Services:**  
   - Set **min instances = 0** for both dispatcher and worker services.  
   - Configure **max instances** modestly (e.g., 5) to bound costs.  
2. **Redis Instance:**  
   - Use the smallest Memorystore tier (single-node).  
   - No high availability until needed.  
3. **Celery Worker Settings:**  
   - Low concurrency (e.g., 2 workers per instance).  
   - `worker_max_tasks_per_child` to avoid memory leaks.  
4. **Email Provider:**  
   - Choose a free-tier SMTP (e.g., Gmail SMTP) or low-cost transactional service.  
5. **Monitoring & Logging:**  
   - Rely on default Cloud Run logs.  
   - No paid monitoring until scale demands.  

**Outcome:**  
An entirely serverless stack that scales to zero between weekly runs, with predictable, minimal costs.

***

### **Extension for Security (Future)**

- **Firestore IAM Roles:** Later assign a service account with Firestore read/write permissions.  
- **Redis ACLs & VPC:** Optionally place Memorystore in a private VPC and restrict access.  
- **Cloud Run IAM:** Later enforce invocation permissions on Cloud Run endpoints.  

***

### **Summary Table**

| Stage                               | Components                                         | Notes                                                 |
|-------------------------------------|----------------------------------------------------|-------------------------------------------------------|
| 1. Infrastructure Provisioning      | Terraform, Cloud Run, Load Balancer, Firestore, Redis, Scheduler | End-to-end cloud footprint automated via IaC |
| 2. Capture & Storage                | Firestore                                          | Simple document CRUD                                  |
| 3. Fixed-Time Trigger               | Cloud Scheduler                                    | One cron job, weekly                                  |
| 4. Batch Dispatcher                 | Cloud Run (dispatcher) + Celery                    | Group by topic, one task per topic                    |
| 5. Processing & Change Detect       | LangChain + Redis (Memorystore)                    | Single-node Redis, baseline comparison                |
| 6. Email Dispatch                   | Celery + SMTP                                      | Plain-text, free/low-cost provider                    |
| 7. Config & Cost Control            | Cloud Run min=0, low-tier Redis, basic logging     | Scales to zero, bounded max instances                 |

***

**Desired Result:**  
A lean, serverless weekly subscription system that runs only once a week, minimizes operational complexity and cost, and remains extensible for future security enhancements.