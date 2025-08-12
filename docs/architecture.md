# Architecture Overview

This document provides a high-level description of the Interactive Search Engine system architecture.

## Current Architecture (Stage 1 - Phase 2 Complete)

The system is designed as a decoupled, containerized architecture with the following components:

### Local Development Environment

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   (Next.js)     │    │   (FastAPI)     │
│   Port: 3000    │    │   Port: 8000    │
│   + UI + State  │    │   + API + Log   │
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
- **Technology:** Next.js with TypeScript and Tailwind CSS
- **Purpose:** User interface, state management, and client-side logic
- **Container:** Development-focused Docker container
- **Port:** 3000 (local development)
- **Features:**
  - Interactive search interface with text input and submit button
  - React state management for input text and results
  - Real-time API communication with backend
  - Error handling and loading states
  - Responsive design with modern UI components
  - Local proxy configuration for seamless API calls

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

### Frontend Architecture

#### User Interface Components
1. **Search Input Section:** Text input field with submit button
2. **Results Display:** Dynamic area showing processed text results
3. **Error Handling:** User-friendly error messages and validation
4. **Loading States:** Visual feedback during API calls
5. **Responsive Design:** Mobile-friendly layout with Tailwind CSS

#### State Management
- **Input State:** Manages current text in search field
- **Result State:** Stores and displays API response data
- **Loading State:** Tracks API call status
- **Error State:** Handles and displays error messages

#### API Communication
- **Fetch Integration:** Uses native fetch API for HTTP requests
- **Request Format:** Sends JSON payload matching backend contract
- **Response Handling:** Parses and displays backend results
- **Error Handling:** Graceful fallback for failed requests
- **Proxy Configuration:** Seamless routing via Next.js rewrites

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

### Local Development Features

- **Single Command Startup:** `docker-compose up` launches entire environment
- **Hot Reloading:** Both frontend and backend support live code updates
- **API Proxy:** Frontend automatically routes `/api/*` requests to backend
- **Cross-Container Communication:** Services communicate via Docker network
- **Development Ports:** Frontend on 3000, Backend on 8000

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
8. **User Experience:** Intuitive interface with real-time feedback
9. **Error Resilience:** Graceful handling of failures and edge cases
