# Perplexity Clone - Interactive Search Engine

A modern, scalable search engine application built with Next.js frontend and FastAPI backend, deployed on Google Cloud Platform with **fully automated CI/CD**.

## 🚀 Current Status

**✅ Phase 1 Complete**: Core search functionality with complete UI skeleton
**🔧 Phase 2**: User management and authentication (planned)
**🔧 Phase 3**: AI search integration (planned)
**🔧 Phase 4**: Advanced features (planned)

### What's Working Now
- **Core Search**: Text processing with exclamation point transformation
- **Complete UI**: Full application interface with all planned features as skeletons
- **Responsive Design**: Mobile-first design that works on all devices
- **Theme Support**: Light/dark mode with persistent storage
- **Infrastructure**: Fully deployed and automatically managed via CI/CD
- **CI/CD Pipeline**: Fully operational with automatic deployments on every code push

### What's Coming Next
- User authentication and profiles
- Real AI-powered search
- Search history persistence
- Advanced search features

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
- React 18 with TypeScript
- Tailwind CSS for styling
- Complete UI skeleton with all planned features
- Core search functionality implemented
- Theme switching and responsive design
- Health check endpoint at `/api/health`
- **Automatically deployed via CI/CD on every code push**

### Backend (FastAPI)
- Python 3.11 with FastAPI
- Search service (`/api/v1/search`)
- Health check endpoint (`/api/v1/health`)
- CORS middleware with configurable origins
- Secure API access (frontend service account only)
- **Automatically deployed via CI/CD on every code push**

### Infrastructure (Terraform + GCP)
- Google Cloud Run services (frontend & backend)
- Google Artifact Registry for Docker images
- Load balancer with SSL termination and HTTP→HTTPS redirect
- Remote state management in GCS bucket
- VPC network and service accounts
- **Automatically updated via CI/CD on every code push**

### CI/CD Pipeline (GitHub Actions)
- **✅ FULLY OPERATIONAL**
- **Automated builds** on every push to main/develop branches
- **Automated testing** and quality checks
- **Automated deployment** to Cloud Run
- **Automated infrastructure** updates via Terraform
- **Comprehensive verification** after deployment
- **Daily security scanning** and maintenance

## 📚 Documentation

- [API Documentation](docs/api.md) - Backend API endpoints and models
- [Architecture Overview](docs/architecture.md) - System design and components
- [Frontend Features](docs/frontend-features.md) - Complete frontend component documentation
- [CI/CD Pipeline](docs/ci-cd.md) - **Fully operational deployment automation**
- [Infrastructure Setup](infrastructure/README.md) - Terraform and GCP setup

## 🌐 Live Demo

- **Frontend**: https://perplexity-clone-frontend-233562799891.us-central1.run.app
- **Load Balancer**: https://34.54.95.184

## 🔄 Deployment Automation

### Zero-Touch Deployments
- **Push to main/develop**: Automatically triggers full CI/CD pipeline
- **Automated testing**: Prevents broken deployments
- **Automated building**: Docker images built and pushed to Artifact Registry
- **Automated deployment**: Services updated on Cloud Run via Terraform
- **Automated verification**: Comprehensive health checks and testing
- **Rollback capability**: Previous versions available for quick recovery

### Current Pipeline Status
- **Status**: ✅ **FULLY OPERATIONAL**
- **Last Deployment**: Automatically triggered on every code push
- **Next Deployment**: Will occur automatically on next code push
- **Security**: Daily automated scanning and maintenance

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
