# Interactive Search Engine

A modern, containerized search engine application built with Next.js frontend and FastAPI backend, designed for cloud deployment on Google Cloud Platform.

## Project Status

**Current Stage:** Stage 0 - Project & Local Environment Setup ✅  
**Next Stage:** Stage 1 - Core API Development with Essential Middleware

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

## Project Structure

```
perplexity-clone/
├── backend/                 # FastAPI backend service
│   ├── src/                # Python source code
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
- FastAPI automatic documentation at `/docs`

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

According to the project plan, the next stage (Stage 1) will implement:
- CORS middleware for frontend-backend communication
- Logging middleware for request tracking
- Authentication placeholder structure
- Core text processing feature endpoint

## Contributing

This project follows a strict phased implementation approach. Please refer to the [project plan](plan.md) for current development priorities and constraints.
