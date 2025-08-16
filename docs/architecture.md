# Architecture Overview

This document provides a high-level description of the Perplexity Clone system architecture.

## System Components

The application follows a modern web architecture with the following main components:

### Frontend (Next.js)
- **Technology:** Next.js 15 with TypeScript and Tailwind CSS
- **Deployment:** Google Cloud Run (automatically deployed via CI/CD)
- **Current Features:** 
  - Responsive two-panel layout (sidebar + main content)
  - Mobile-first design with hamburger menu
  - Core search functionality with text processing
  - Search suggestions and result display
  - Theme switching (light/dark mode)
  - Toast notifications for "Coming Soon" features
- **UI Skeleton Components:**
  - Search history display (static data)
  - User profile page (placeholder functionality)
  - Settings page (placeholder functionality)
  - Help/Support page (placeholder functionality)

### Backend (FastAPI)
- **Technology:** Python FastAPI with async support
- **Deployment:** Google Cloud Run (automatically deployed via CI/CD)
- **Current Features:**
  - Health check endpoint (`/api/v1/health`)
  - Search endpoint (`/api/v1/search`)
  - CORS middleware with configurable origins
  - Global exception handling and logging
  - Request/response validation with Pydantic models
- **Future Features:** Authentication, user management, AI search

### Infrastructure (Terraform)
- **Cloud Provider:** Google Cloud Platform
- **Deployed Services:**
  - Cloud Run for frontend and backend
  - Load Balancer with SSL termination and HTTP→HTTPS redirect
  - Google Artifact Registry for container images
  - VPC network and subnets
  - Service accounts for secure communication
  - Remote state storage in GCS bucket
- **Current Status:** Fully deployed and automatically managed via CI/CD

### CI/CD Pipeline (GitHub Actions)
- **Status:** ✅ **FULLY OPERATIONAL**
- **Automation:** Automatically builds and deploys on every code push
- **Features:**
  - Automated Docker image building and pushing
  - Automated testing and quality checks
  - Automated deployment to Cloud Run
  - Automated infrastructure updates via Terraform
  - Comprehensive post-deployment verification
  - Daily security scanning and maintenance

## Component Interaction

```
User → Load Balancer (HTTPS) → Frontend (Cloud Run)
                    ↓
                Backend (Cloud Run) → [Future: Database]
```

### Current Data Flow
1. **Frontend Search**: User types query in search input
2. **API Proxy**: Frontend Next.js API route proxies request to backend
3. **Backend Processing**: FastAPI processes text and adds exclamation points
4. **Response**: Result displayed in the UI with loading states and error handling

### CI/CD Flow
1. **Code Push**: Developer pushes to main/develop branch
2. **Automated Build**: GitHub Actions builds Docker images
3. **Image Push**: Images automatically pushed to Artifact Registry
4. **Automated Deploy**: Terraform deploys new images to Cloud Run
5. **Verification**: Comprehensive testing and health checks
6. **Live Update**: Services automatically updated with new code

## Design Principles

1. **Responsive Design:** Mobile-first approach with progressive enhancement
2. **Component Architecture:** Modular, reusable components with clear separation of concerns
3. **Future-Ready:** UI skeleton includes all planned features with "Coming Soon" placeholders
4. **Performance:** Optimized for fast loading and smooth user experience
5. **Accessibility:** ARIA attributes and keyboard navigation support
6. **Security:** Backend not publicly accessible, frontend-only communication
7. **Automation:** Full CI/CD pipeline for zero-touch deployments

## Technology Stack

- **Frontend:** Next.js 15, React 18, TypeScript, Tailwind CSS, react-hot-toast
- **Backend:** Python 3.11+, FastAPI, Pydantic, uvicorn
- **Infrastructure:** Terraform, Google Cloud Platform, Cloud Run, Artifact Registry
- **CI/CD:** GitHub Actions (fully operational with automated deployments)
- **Database:** Not yet implemented (planned for future phases)

## Current Deployment Status

### Services
- **Frontend URL:** https://perplexity-clone-frontend-233562799891.us-central1.run.app
- **Backend URL:** https://perplexity-clone-backend-233562799891.us-central1.run.app (private)
- **Load Balancer:** http://34.54.95.184 (HTTP) / https://34.54.95.184 (HTTPS)

### Security
- **Frontend:** Public access enabled
- **Backend:** Service account access only (not publicly accessible)
- **CORS:** Properly configured for frontend-backend communication
- **State Management:** Remote Terraform state in private GCS bucket

### CI/CD Status
- **Pipeline:** Fully operational and automatically running
- **Deployments:** Automatic on every push to main/develop branches
- **Testing:** Comprehensive automated testing and verification
- **Security:** Daily automated security scanning and maintenance

## Future Architecture Components

### Phase 2: User Management & Authentication
- User database (PostgreSQL)
- Authentication service (JWT-based)
- User profile management
- Search history persistence

### Phase 3: AI Search Integration
- AI model integration
- Web scraping capabilities
- Search result caching
- Advanced search algorithms

### Phase 4: Advanced Features
- Subscription management
- API rate limiting
- Analytics and monitoring
- Multi-language support

## Deployment Automation

The system is designed for **zero-touch deployments**:

1. **Developer Experience**: Simply push code to trigger full deployment
2. **Quality Gates**: Automated testing prevents broken deployments
3. **Rollback Capability**: Previous image versions available for quick recovery
4. **Environment Consistency**: All environments managed identically via Terraform
5. **Security First**: Automated security scanning on every deployment
