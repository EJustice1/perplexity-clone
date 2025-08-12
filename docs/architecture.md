# Architecture Overview

This document provides a high-level description of the Interactive Search Engine system architecture.

## Current Architecture (Stage 1)

The system is designed as a decoupled, containerized architecture with the following components:

### Local Development Environment

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   (Next.js)     │    │   (FastAPI)     │
│   Port: 3000    │    │   Port: 8000    │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────────────────┘
                    │
         ┌─────────────────┐
         │ Docker Compose  │
         │   (Local Dev)   │
         └─────────────────┘
```

### Service Descriptions

#### Frontend Service
- **Technology:** Next.js with TypeScript
- **Purpose:** User interface and client-side logic
- **Container:** Development-focused Docker container
- **Port:** 3000 (local development)

#### Backend Service
- **Technology:** FastAPI (Python)
- **Purpose:** API server and business logic
- **Container:** Python-based Docker image
- **Port:** 8000 (local development)
- **Features:**
  - CORS middleware for frontend communication
  - Custom logging middleware for request tracking
  - Authentication placeholder structure
  - Core text processing endpoint (`/api/v1/process-text`)

### Backend Architecture

#### Middleware Stack
1. **CORS Middleware:** Enables cross-origin requests from frontend
2. **Logging Middleware:** Custom middleware for request logging and monitoring
3. **Authentication Placeholder:** Security pattern established for future implementation

#### API Endpoints
- **Health Check:** `GET /health` - Service status verification
- **Text Processing:** `POST /api/v1/process-text` - Core feature implementation

#### Data Models
- **TextProcessRequest:** Input validation for text processing
- **TextProcessResponse:** Structured response format
- **Error Handling:** Proper HTTP status codes and error messages

### Containerization Strategy

- **Backend:** Single-stage Python container with FastAPI and Uvicorn
- **Frontend:** Development container with Node.js and Next.js
- **Development:** Volume mounts for hot-reloading and code changes

## Future Architecture (Planned)

The system is designed to scale to Google Cloud Platform with:

- **Cloud Run Services:** Containerized services running on GCP
- **Load Balancer:** Global HTTPS load balancer with path-based routing
- **Artifact Registry:** Docker image storage and versioning
- **CI/CD Pipeline:** Automated deployment via GitHub Actions

## Design Principles

1. **Decoupled Services:** Frontend and backend are completely independent
2. **Container-First:** All services are containerized from the start
3. **Local Development:** Full local environment with single command startup
4. **Future-Ready:** Architecture supports planned cloud deployment
5. **Standards-Based:** Uses industry-standard technologies and patterns
6. **Observability:** Built-in logging and monitoring capabilities
7. **Security-First:** Authentication patterns established early
