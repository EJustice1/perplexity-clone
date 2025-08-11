# Perplexity Clone

A modern, AI-powered search application built with FastAPI backend and Next.js frontend, featuring a clean, extensible middleware architecture.

## 🏗️ Project Structure

```
perplexity-clone/
├── backend/                    # FastAPI backend service
│   ├── src/                   # Python source code
│   ├── tests/                 # Backend tests
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend container
│   └── pyproject.toml        # Python project config
├── frontend/                  # Next.js frontend service
│   ├── src/                  # Next.js source code
│   ├── public/               # Static assets
│   ├── package.json          # Node dependencies
│   └── Dockerfile            # Frontend container
├── infrastructure/            # Infrastructure as Code
│   ├── terraform/            # Terraform configurations
│   ├── docker/               # Docker compose and orchestration
│   └── monitoring/           # Prometheus, Grafana configs
├── scripts/                   # Build and utility scripts
├── docs/                      # Documentation
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- **Backend**: Python 3.8+, Docker
- **Frontend**: Node.js 18+, npm
- **Infrastructure**: Docker Compose, Terraform (optional)

### Local Development

```bash
# Clone the repository
git clone https://github.com/your-org/perplexity-clone.git
cd perplexity-clone

# Backend
cd backend
pip install -e .
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (new terminal)
cd ../frontend
npm install
npm run dev

# Infrastructure (optional)
cd ../infrastructure/docker
docker-compose up -d
```

### Using Docker

```bash
# Start all services
cd infrastructure/docker
docker-compose up -d

# Access services
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# Grafana: http://localhost:3001
# Prometheus: http://localhost:9090
```

## 🏛️ Architecture

### Backend (FastAPI)

- **Framework**: FastAPI with async support
- **Middleware**: Extensible system for metrics, auth, caching
- **Monitoring**: Prometheus metrics and health checks
- **Documentation**: Auto-generated OpenAPI docs

### Frontend (Next.js)

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS for responsive design
- **Type Safety**: Full TypeScript support
- **Performance**: Built-in optimization and code splitting

### Middleware System

The application features a clean, extensible middleware architecture:

- **Base Classes**: Abstract interfaces for all middleware
- **Framework Support**: FastAPI and Flask implementations
- **Metrics**: Built-in Prometheus integration
- **Extensible**: Easy to add new middleware types

## 🔧 Development

### Backend Development

```bash
cd backend

# Install dependencies
pip install -e .

# Run tests
pytest

# Code quality
black src/
isort src/
flake8 src/
mypy src/

# Run development server
uvicorn src.api.main:app --reload
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Code quality
npm run lint
npm run type-check
```

### Adding New Middleware

1. Create new middleware class inheriting from `BaseMiddleware`
2. Implement required methods (`process_request`, `process_response`)
3. Add framework-specific implementations if needed
4. Update package exports and configuration

## 🚀 Deployment

### Backend Deployment

```bash
# Build Docker image
cd backend
docker build -t perplexity-backend .

# Run container
docker run -p 8000:8000 perplexity-backend
```

### Frontend Deployment

```bash
# Build for production
cd frontend
npm run build

# Deploy to Vercel (recommended)
vercel --prod

# Or use Docker
docker build -t perplexity-frontend .
docker run -p 3000:3000 perplexity-frontend
```

### Infrastructure Deployment

```bash
# Deploy with Terraform
cd infrastructure/terraform
terraform init
terraform plan
terraform apply

# Or use Docker Compose
cd infrastructure/docker
docker-compose -f docker-compose.prod.yml up -d
```

## 📊 Monitoring

### Built-in Metrics

- **Request Count**: Total requests by method, endpoint, status
- **Latency**: Request duration histograms
- **Health Checks**: Service status monitoring
- **Custom Metrics**: Extensible for business logic

### Monitoring Stack

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Alerts**: Configurable alerting rules

## 🔒 Security

- **CORS**: Configurable cross-origin policies
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Secure error responses
- **Monitoring**: Security event tracking

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Follow** the established patterns
4. **Add** tests for new functionality
5. **Update** documentation
6. **Submit** a pull request

### Development Guidelines

- Use type hints throughout
- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript
- Write comprehensive docstrings
- Include error handling

## 📚 Documentation

- **Backend**: [Backend README](backend/README.md)
- **Frontend**: [Frontend README](frontend/README.md)
- **Infrastructure**: [Infrastructure README](infrastructure/README.md)
- **Scripts**: [Scripts README](scripts/README.md)
- **API**: Interactive docs at `/docs` when backend is running

## 🐛 Troubleshooting

### Common Issues

1. **Port Conflicts**: Check if ports 8000, 3000, 9090, 3001 are available
2. **Docker Issues**: Ensure Docker and Docker Compose are running
3. **Dependencies**: Verify Python and Node.js versions
4. **Environment**: Check environment variable configuration

### Getting Help

- Check service logs
- Review configuration files
- Verify network connectivity
- Check resource usage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent backend framework
- Next.js for the modern frontend framework
- Prometheus and Grafana for monitoring
- The open source community for inspiration

---

**Built with ❤️ using modern web technologies and best practices**
