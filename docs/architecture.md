# Architecture Overview

This document provides a high-level description of the Interactive Search Engine system architecture.

## Current Architecture (Stage 1 - Phase 3 Complete)

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

### Cloud Production Environment

```
┌─────────────────────────────────────────────────────────────┐
│                    Global Load Balancer                     │
│                    (HTTPS + SSL)                           │
│                    Path-based Routing                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
    ┌────▼────┐              ┌────▼────┐
    │Frontend │              │Backend  │
    │Cloud Run│              │Cloud Run│
    │Service  │              │Service  │
    └─────────┘              └─────────┘
         │                         │
         └─────────────────────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
    ┌────▼────┐              ┌────▼────┐
    │Artifact │              │Secret   │
    │Registry │              │Manager  │
    └─────────┘              └─────────┘
```

### Service Descriptions

#### Frontend Service
- **Technology:** Next.js with TypeScript and Tailwind CSS
- **Purpose:** User interface, state management, and client-side logic
- **Container:** Development-focused Docker container (local) / Cloud Run (production)
- **Port:** 3000 (local development) / Auto-assigned (Cloud Run)
- **Features:**
  - Interactive search interface with text input and submit button
  - React state management for input text and results
  - Real-time API communication with backend
  - Error handling and loading states
  - Responsive design with modern UI components
  - Local proxy configuration for seamless API calls (local)
  - Environment-based API URL configuration (production)

#### Backend Service
- **Technology:** FastAPI (Python)
- **Purpose:** API server and business logic
- **Container:** Python-based Docker image (local) / Cloud Run (production)
- **Port:** 8000 (local development) / Auto-assigned (Cloud Run)
- **Features:**
  - CORS middleware for frontend communication
  - Custom logging middleware for request tracking
  - Authentication placeholder structure
  - Core text processing endpoint (`/api/v1/process-text`)

### Cloud Infrastructure Components

#### Google Artifact Registry
- **Purpose:** Centralized Docker image storage
- **Features:** Version control, security scanning, regional replication
- **Integration:** Cloud Run services pull images from this registry

#### Google Secret Manager
- **Purpose:** Secure storage for application secrets
- **Features:** Encryption at rest, IAM integration, audit logging
- **Integration:** Cloud Run services access secrets via service account

#### Cloud Run Services
- **Purpose:** Serverless container execution
- **Features:** Auto-scaling, zero-to-scale, HTTPS endpoints
- **Configuration:** Resource limits, environment variables, service accounts

#### Global Load Balancer
- **Purpose:** Traffic distribution and SSL termination
- **Features:** Path-based routing, managed SSL certificates, global distribution
- **Routing Rules:**
  - `/api/*` → Backend Cloud Run service
  - All other paths → Frontend Cloud Run service

#### VPC Network
- **Purpose:** Isolated network for load balancer components
- **Features:** Custom subnets, firewall rules, network policies
- **Security:** Isolated from default VPC, minimal exposure

#### Service Account
- **Purpose:** Identity and permissions for Cloud Run services
- **Features:** Minimal permissions principle, IAM integration
- **Roles:** Cloud Run invoker, logging writer, monitoring writer, secret accessor

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
- **Proxy Configuration:** Seamless routing via Next.js rewrites (local)
- **Environment Configuration:** Dynamic API URL based on environment (production)

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
- **Frontend:** Development container with Node.js and Next.js (local) / Production build (Cloud Run)
- **Development:** Volume mounts for hot-reloading and code changes
- **Production:** Optimized images with minimal dependencies

### Local Development Features

- **Single Command Startup:** `docker-compose up` launches entire environment
- **Hot Reloading:** Both frontend and backend support live code updates
- **API Proxy:** Frontend automatically routes `/api/*` requests to backend
- **Cross-Container Communication:** Services communicate via Docker network
- **Development Ports:** Frontend on 3000, Backend on 8000

### Production Features

- **Auto-scaling:** Cloud Run services scale from 0 to 10 instances based on demand
- **Global Distribution:** Load balancer distributes traffic globally
- **SSL Termination:** Managed HTTPS certificates with automatic renewal
- **Health Monitoring:** Built-in health checks for both services
- **Logging & Monitoring:** Integrated with Google Cloud Operations
- **Security:** Service accounts with minimal required permissions

## Future Architecture (Planned)

The system is designed to scale with:

- **CI/CD Pipeline:** Automated deployment via GitHub Actions (Phase 4)
- **Monitoring & Alerting:** Advanced observability and alerting
- **Database Integration:** User profiles and subscription management
- **Content Processing:** Web scraping and content analysis features

## Design Principles

1. **Decoupled Services:** Frontend and backend are completely independent
2. **Container-First:** All services are containerized from the start
3. **Local Development:** Full local environment with single command startup
4. **Cloud-Native:** Designed for Google Cloud Platform from the beginning
5. **Standards-Based:** Uses industry-standard technologies and patterns
6. **Observability:** Built-in logging and monitoring capabilities
7. **Security-First:** Authentication patterns and minimal permissions
8. **User Experience:** Intuitive interface with real-time feedback
9. **Error Resilience:** Graceful handling of failures and edge cases
10. **Cost Optimization:** Serverless architecture with pay-per-use pricing
11. **Scalability:** Auto-scaling services with global load distribution
