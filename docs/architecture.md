# Architecture Overview

This document provides a high-level description of the Perplexity Clone system architecture.

## System Components

The application follows a modern web architecture with the following main components:

### Frontend (Next.js)
- **Technology:** Next.js 15 with TypeScript and Tailwind CSS
- **Deployment:** Google Cloud Run
- **Features:** 
  - Responsive two-panel layout (sidebar + main content)
  - Mobile-first design with hamburger menu
  - Static UI skeleton for future features
  - Toast notifications for "Coming Soon" features

### Backend (FastAPI)
- **Technology:** Python FastAPI with async support
- **Deployment:** Google Cloud Run
- **Features:**
  - RESTful API endpoints
  - Text processing service
  - Health check endpoint
  - Future: Authentication, user management, AI search

### Infrastructure (Terraform)
- **Cloud Provider:** Google Cloud Platform
- **Services:**
  - Cloud Run for frontend and backend
  - Load Balancer for traffic distribution
  - Cloud SQL for future database needs
  - Service accounts for secure communication

## Component Interaction

```
User → Load Balancer → Frontend (Cloud Run)
                    ↓
                Backend (Cloud Run) → Database (Future)
```

## Design Principles

1. **Responsive Design:** Mobile-first approach with progressive enhancement
2. **Component Architecture:** Modular, reusable components with clear separation of concerns
3. **Future-Ready:** UI skeleton includes all planned features with "Coming Soon" placeholders
4. **Performance:** Optimized for fast loading and smooth user experience
5. **Accessibility:** ARIA attributes and keyboard navigation support

## Technology Stack

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Backend:** Python, FastAPI, SQLAlchemy (future)
- **Database:** PostgreSQL (future)
- **Infrastructure:** Terraform, Google Cloud Platform
- **CI/CD:** GitHub Actions (future)
