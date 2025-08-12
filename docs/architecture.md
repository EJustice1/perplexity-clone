# Architecture Overview

This document provides a high-level description of the Interactive Search Engine system architecture.

## Current Architecture (Stage 0)

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
- **Container:** Multi-stage Docker build for production optimization
- **Port:** 3000 (local development)

#### Backend Service
- **Technology:** FastAPI (Python)
- **Purpose:** API server and business logic
- **Container:** Python-based Docker image
- **Port:** 8000 (local development)

### Containerization Strategy

- **Backend:** Single-stage Python container with FastAPI and Uvicorn
- **Frontend:** Multi-stage container with Node.js build process and production-optimized runtime
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
