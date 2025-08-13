# Interactive Search Engine

A modern, containerized search engine application built with Next.js frontend and FastAPI backend, designed for cloud deployment on Google Cloud Platform.

## Project Status

**Current Stage:** Stage 1 - Core API Development with Essential Middleware ✅  
**Next Stage:** Stage 2 - Frontend Development & Full Local Integration

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd perplexity-clone
   ```

2. **Start the local environment:**
   ```bash
   docker-compose up
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Health Check: http://localhost:8000/health
   - API Documentation: http://localhost:8000/docs

## Project Structure

```
perplexity-clone/
├── backend/                 # FastAPI backend service
│   ├── src/                # Python source code
│   │   ├── main.py         # Main application with API endpoints
│   │   ├── middleware.py   # Custom logging middleware
│   │   └── auth.py         # Authentication placeholder
│   ├── Dockerfile          # Backend container definition
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend application
│   ├── src/                # React source code
│   ├── Dockerfile          # Frontend container definition
│   └── package.json        # Node.js dependencies
├── infrastructure/         # Terraform and cloud configuration
├── docs/                   # Project documentation
│   ├── api.md             # API endpoint documentation
│   └── architecture.md    # System architecture overview
├── docker-compose.yml      # Local development environment
└── plan.md                # Project implementation plan
```

## Development

### Backend Development

The backend is a FastAPI application running on port 8000. The source code is mounted as a volume, so changes are reflected immediately.

**Current Features:**
- Health check endpoint (`/health`)
- CORS middleware for frontend communication
- Custom logging middleware for request tracking
- Authentication placeholder structure
- Core text processing endpoint (`/api/v1/process-text`)
- FastAPI automatic documentation at `/docs`

**API Endpoints:**
- `GET /health` - Service health verification
- `POST /api/v1/process-text` - Text processing with exclamation points

### Frontend Development

The frontend is a Next.js application with TypeScript and Tailwind CSS. It runs on port 3000 with hot-reloading enabled.

**Current Features:**
- Next.js 14 with App Router
- TypeScript support
- Tailwind CSS for styling
- ESLint configuration

## Documentation

- [API Documentation](docs/api.md) - Complete API endpoint reference
- [Architecture Overview](docs/architecture.md) - System design and architecture
- [Project Plan](plan.md) - Detailed implementation roadmap

## Next Steps

According to the project plan, the next stage (Stage 2) will implement:
- Frontend UI components for text input and display
- State management for user interactions
- API communication between frontend and backend
- Local proxy configuration for seamless development

## Contributing

This project follows a strict phased implementation approach. Please refer to the [project plan](plan.md) for current development priorities and constraints.
# Test CI/CD fix
