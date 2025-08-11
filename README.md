# Perplexity Clone

A modern AI-powered search application built with FastAPI backend and Next.js frontend, featuring comprehensive monitoring and middleware architecture.

## 🚀 Project Overview

This project aims to create a Perplexity-like search experience with:
- **AI-powered search** with context understanding
- **Real-time results** from multiple sources
- **Professional monitoring** with Prometheus and Grafana
- **Scalable architecture** with clean middleware design
- **Modern frontend** built with Next.js and TypeScript

## 🏗️ Architecture

```
perplexity-clone/
├── src/
│   ├── api/                  # FastAPI backend
│   ├── frontend/             # Next.js frontend (TypeScript + Tailwind)
│   ├── core/                 # Core utilities and configuration
│   └── middleware/           # Expandable middleware system
├── prometheus/               # Monitoring configuration
├── grafana/                  # Dashboard and provisioning
├── terraform/                # Infrastructure as code
└── docker-compose.yml        # Multi-service orchestration
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Prometheus** - Metrics collection
- **Python** - Core application logic

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client for API integration

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-service orchestration
- **Prometheus** - Monitoring and alerting
- **Grafana** - Visualization and dashboards

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.8+ (for backend development)

### 1. Start All Services
```bash
docker-compose up -d
```

### 2. Access Services
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Grafana**: http://localhost:3001
- **Prometheus**: http://localhost:9090

### 3. Development Mode
```bash
# Backend development
cd src/api
uvicorn main:app --reload

# Frontend development
cd src/frontend
npm run dev
```

## 📁 Project Structure

### Backend (`src/api/`)
- FastAPI application with health and metrics endpoints
- Integrated with Prometheus monitoring
- Clean middleware architecture

### Frontend (`src/frontend/`)
- Next.js 14 application with TypeScript
- Modern search interface with responsive design
- API integration with FastAPI backend
- Professional UI components

### Core (`src/core/`)
- Centralized configuration management
- Utility functions and common logic
- Environment-based settings

### Middleware (`src/middleware/`)
- Expandable middleware architecture
- Metrics collection (fully implemented)
- Framework-agnostic design
- Ready for future enhancements (auth, caching, rate limiting)

## 🔍 Features

### Search Capabilities
- **AI-powered search** with context understanding
- **Real-time results** from multiple sources
- **Smart suggestions** and auto-complete
- **Relevance scoring** for better results

### Monitoring & Observability
- **Prometheus metrics** collection
- **Grafana dashboards** for visualization
- **Health checks** for all services
- **Performance monitoring** and alerting

### Architecture Benefits
- **Scalable design** with clean separation of concerns
- **Middleware system** for easy feature addition
- **Type safety** throughout the stack
- **Professional deployment** ready

## 🚀 Development

### Backend Development
```bash
cd src/api
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd src/frontend
npm install
npm run dev
```

### Monitoring Setup
```bash
./setup-monitoring.sh
./test-monitoring.sh
```

## 🐳 Docker

### Build and Run
```bash
# Build all services
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Build
```bash
./build.sh
```

## 📊 Monitoring

### Prometheus
- HTTP request metrics
- Service health monitoring
- Custom alerting rules
- Service discovery

### Grafana
- Pre-configured dashboards
- Real-time metrics visualization
- Service health overview
- Performance analytics

## 🔮 Future Enhancements

- **Authentication system** with JWT
- **Caching layer** with Redis
- **Rate limiting** and DDoS protection
- **Advanced search filters** and sorting
- **User search history** and preferences
- **Real-time updates** with WebSockets
- **Multi-language support**
- **Mobile app** development

## 🤝 Contributing

1. **Follow the established patterns** in the codebase
2. **Use TypeScript** for frontend development
3. **Maintain clean architecture** and separation of concerns
4. **Add comprehensive tests** for new features
5. **Update documentation** for any changes

## 📚 Documentation

- [Middleware Architecture](MIDDLEWARE_ARCHITECTURE.md) - Detailed middleware design
- [Monitoring Setup](MONITORING.md) - Prometheus and Grafana configuration
- [Frontend README](src/frontend/README.md) - Next.js frontend documentation

## 🐛 Troubleshooting

### Common Issues
- **Port conflicts**: Check if ports 3000, 8000, 3001, 9090 are available
- **Docker issues**: Ensure Docker is running and has sufficient resources
- **API connection**: Verify backend is running and accessible
- **Build errors**: Check Node.js version and npm dependencies

### Getting Help
- Check service logs: `docker-compose logs [service-name]`
- Verify service health: Visit health endpoints
- Check browser console for frontend errors
- Review Prometheus targets for monitoring issues

---

**Built with modern technologies and best practices for scalability and maintainability** 🚀
