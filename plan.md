Of course. Here is the standalone project plan, maintaining the same structure but with expanded descriptions of the specific frontend and backend functionality for the initial feature.

***

### **Project Implementation Plan: Interactive Search Engine (Stage 1 Foundation)**

**Objective:** To implement the foundational architecture and a minimal viable feature for the Interactive Search Engine project. This plan details the creation of a simple user-facing application, supported by a fully automated, observable, and scalable system on the Google Cloud Platform, preparing it for future expansion.

---

### **Phase 0: Project & Local Environment Setup**

**Goal:** To establish the complete project structure and a fully containerized local development environment, ensuring the architecture is sound before any feature-specific code is written.

**Tasks:**

1.  **Initialize Git Repository:** Create a new monorepo-style project and host it on GitHub.
2.  **Define Directory Structure:** Create a top-level directory structure to cleanly separate the decoupled services: `backend/`, `frontend/`, and `infrastructure/`.
3.  **Initialize Applications:**
    *   **Backend:** Create a minimal FastAPI application within the `backend/src` directory, including a basic `/health` health-check endpoint.
    *   **Frontend:** Initialize a new Next.js project with TypeScript in the `frontend/` directory.
4.  **Create Dockerfiles:**
    *   **Backend:** Develop a `Dockerfile` for the FastAPI service that installs dependencies and runs the application server.
    *   **Frontend:** Develop a multi-stage `Dockerfile` for the Next.js service that builds the application for production and serves it.
5.  **Configure Local Environment:** Create a `docker-compose.yml` file in the project root. This file will define the `frontend` and `backend` services, allowing the entire local environment to be launched with a single command.

**Desired Result:** A developer can clone the repository, run `docker-compose up`, and have both the Next.js frontend and FastAPI backend running and accessible on their local machine. The project is fully containerized and ready for feature development.

---

### **Phase 1: Core API Development with Essential Middleware**

**Goal:** To build a robust and extensible backend API that incorporates critical middleware for logging and future security needs, followed by the implementation of the core "exclamation point" feature logic.

**Tasks:**

1.  **Implement CORS Middleware:** Integrate FastAPI's built-in CORS middleware to allow the frontend application to make requests to the backend API.
2.  **Implement Logging Middleware:** Create a custom middleware that intercepts every request to log key information (method, path, status code, and processing time) to the console, fulfilling the structured logging requirement (`NFR4.3`).
3.  **Establish Authentication Placeholder:** Create a new file (`auth.py`) to serve as a placeholder for future authentication logic, establishing the security pattern early.
4.  **Implement Core Feature Endpoint:**
    *   **Definition:** Define a `POST` endpoint at the path `/api/v1/process-text`.
    *   **Request Contract:** This endpoint will expect a JSON object in the request body with a single key: `{"text": "some user input"}`.
    *   **Backend Logic:** Upon receiving a request, the endpoint will extract the string value from the `text` field. It will then transform this string by prepending and appending `!!! ` (with a space).
    *   **Response Contract:** The endpoint will return a JSON object with a single key containing the modified string: `{"result": "!!! some user input !!!"}`.

**Desired Result:** The backend API is fully functional. It exposes a well-defined endpoint that accepts a JSON object, processes the text as specified, and returns a new JSON object with the result. All API calls are automatically logged, and the architecture is prepared for future security extensions.

---

### **Phase 2: Frontend Development & Full Local Integration**

**Goal:** To build the user-facing interface and connect it to the backend, creating a complete, end-to-end user experience for the "exclamation point" feature.

**Tasks:**

1.  **Build UI Components:** In the Next.js application, create the visual elements for user interaction: a text input element (the "search bar"), a clickable "Submit" button, and a designated text area on the page where results will be displayed.
2.  **Manage Frontend State:** Utilize React hooks to manage the data within the component, including the current text inside the search bar and the result string received from the backend.
3.  **Implement API Communication:**
    *   **Trigger:** An event handler will be attached to the "Submit" button's click event.
    *   **Action:** When clicked, this handler will read the current text from the search bar state, create a JSON object in the required format (`{"text": "..."}`), and send it as the body of a `POST` request to the backend's `/api/v1/process-text` endpoint.
    *   **Result Handling:** Upon receiving a successful response from the API, the handler will parse the response JSON, extract the value from the `result` key, and update the frontend's result state. This state change will cause the UI to re-render, displaying the new text in the result area.
4.  **Configure Local Proxy:** Modify the `next.config.js` file to include a rewrite rule that proxies requests from the browser to `/api/*` over to the backend container, enabling seamless local development.

**Desired Result:** The application is fully interactive. A user can navigate to the webpage, type "hello world" into the search bar, click the "Submit" button, and see the text "!!! hello world !!!" appear in the result area on the same page.

---

### **Phase 3: Cloud Infrastructure Provisioning with Terraform**

**Goal:** To define and deploy all necessary cloud resources on Google Cloud Platform (GCP) using Infrastructure as Code (IaC), ensuring a repeatable and reliable production environment.

**Tasks:**

1.  **Initialize Terraform Project:** Set up the Terraform configuration files and configure a GCS bucket for remote state management.
2.  **Define Core Resources:** Write Terraform code to provision Google Artifact Registry (for Docker images) and Google Secret Manager (for future secrets).
3.  **Define Application Services:** Define two distinct Cloud Run services (`frontend` and `backend`) and a Global External HTTPS Load Balancer with a Google-managed SSL certificate.
4.  **Configure Traffic Routing:** Configure the load balancer with path-based routing rules to direct `/api/*` traffic to the backend service and all other traffic to the frontend service.
5.  **Deploy Infrastructure:** Execute `terraform apply` to create all the defined resources within the target GCP project.

**Desired Result:** All cloud infrastructure is successfully provisioned, defined as code, and visible in the GCP console. The environment is ready to host the application and requires no manual configuration.

---

### **Phase 4: CI/CD Automation with GitHub Actions**

**Goal:** To create a complete, zero-touch Continuous Integration and Continuous Deployment (CI/CD) pipeline that automatically builds and deploys the application upon code changes.

**Tasks:**

1.  **Create GitHub Actions Workflow:** Define a workflow file in the `.github/workflows/` directory that triggers on any push to the `main` branch.
2.  **Configure Secure Authentication:** Create a GCP Service Account for the CI/CD pipeline and store its credentials as a secure secret in the GitHub repository.
3.  **Define Build & Push Job:** Create a pipeline job to check out code, authenticate with GCP, build the `backend` and `frontend` Docker images, tag them, and push them to Google Artifact Registry.
4.  **Define Deploy Job:** Create a second job that, upon successful build, deploys the newly built images to their respective `backend` and `frontend` Cloud Run services.
5.  **Trigger and Verify:** Commit and push all project code to the `main` branch to trigger the first automated deployment.

**Desired Result:** Any push to the `main` branch automatically triggers the CI/CD pipeline, deploying the application to GCP. The application is live on the internet, and the "no click-ops" requirement is met, establishing a fully automated path from code to production.