# Perplexity Clone - Interactive Search Engine

A modern, scalable search engine application built with Next.js frontend and FastAPI backend, deployed on Google Cloud Platform.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Google Cloud CLI
- Docker

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd perplexity-clone

# Install all dependencies
npm run install:all

# Set up environment variables
cp infrastructure/terraform.tfvars.example infrastructure/terraform.tfvars
# Edit terraform.tfvars with your GCP project details
```

### Development
```bash
# Run both frontend and backend concurrently
npm run dev

# Or run individually
npm run dev:frontend    # Frontend on http://localhost:3000
npm run dev:backend     # Backend on http://localhost:8000
```

## 🧪 Testing

### Run All Tests Concurrently
```bash
npm test                    # Run all tests concurrently (default)
npm run test:concurrent    # Same as above
```

### Run Tests Sequentially
```bash
npm run test:sequential    # Run tests one after another
```

### Run Individual Test Suites
```bash
npm run test:backend       # Backend tests only
npm run test:frontend      # Frontend tests only
```

### Alternative Test Commands
```bash
# Using the shell script directly
./run-tests.sh             # Concurrent (default)
./run-tests.sh sequential  # Sequential
./run-tests.sh backend     # Backend only
./run-tests.sh frontend    # Frontend only
./run-tests.sh help        # Show all options
```

### Test Results
- **Backend**: 18 tests passing (API endpoints, text processing, routing)
- **Frontend**: ESLint passing (no test framework configured yet)
- **Coverage**: Backend tests include coverage reporting

## 🏗️ Architecture

### Frontend (Next.js 15)
- React 19 with TypeScript
- Tailwind CSS for styling
- API integration with backend
- Health check endpoint at `/api/health`

### Backend (FastAPI)
- Python 3.11 with FastAPI
- Text processing service
- Health check endpoints at `/health` and `/api/v1/health`
- Secure API access (frontend service account only)

### Infrastructure (Terraform + GCP)
- Google Cloud Run services
- Google Artifact Registry for Docker images
- Load balancer with SSL termination
- Remote state management in GCS

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Architecture Overview](docs/architecture.md)
- [CI/CD Pipeline](docs/ci-cd.md)
- [Infrastructure Setup](infrastructure/README.md)

## 🔧 Development Commands

```bash
# Build both applications
npm run build

# Start production services
npm start

# Lint both codebases
npm run lint

# Install dependencies
npm run install:all
```

## 🚀 Deployment

The application is deployed on Google Cloud Platform with automated CI/CD:

1. **Infrastructure**: Deployed via Terraform
2. **Services**: Running on Cloud Run
3. **Images**: Stored in Artifact Registry
4. **CI/CD**: Automated via GitHub Actions

See [infrastructure/README.md](infrastructure/README.md) for detailed deployment instructions.

## 📊 Current Status

✅ **Infrastructure**: Fully deployed and secure  
✅ **Remote State**: Working with GCS backend  
✅ **Security**: Backend restricted, frontend public  
✅ **CI/CD Pipeline**: Ready for automated deployments  
✅ **Artifact Registry**: Fully operational with images  
✅ **Health Checks**: Configured and working  
✅ **Testing**: Concurrent test runner operational  

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests: `npm test`
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
