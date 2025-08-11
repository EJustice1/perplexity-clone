# 🚀 Perplexity Clone - Startup Guide

## 🎯 Quick Start

### **Option 1: Start Frontend Only (Recommended for Development)**
```bash
# From project root
npm run frontend:dev
```
**Access at**: http://localhost:3000

### **Option 2: Start Backend Only**
```bash
# From project root
npm run backend:dev
```
**Access at**: http://localhost:8000

### **Option 3: Start Both Frontend and Backend**
```bash
# From project root
npm run dev
```
**Access at**: 
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### **Option 4: Start Everything with Docker**
```bash
# From project root
npm run docker:up
```
**Access at**:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Grafana: http://localhost:3001
- Prometheus: http://localhost:9090

## 🔧 Available Commands

### **Frontend Commands**
```bash
npm run frontend:dev      # Start frontend development server
npm run frontend:build    # Build frontend for production
npm run frontend:start    # Start production frontend server
npm run frontend:install  # Install frontend dependencies
```

### **Backend Commands**
```bash
npm run backend:dev       # Start backend development server
npm run backend:install   # Install backend dependencies
```

### **Docker Commands**
```bash
npm run docker:up         # Start all services
npm run docker:down       # Stop all services
npm run docker:build      # Build all Docker images
npm run docker:logs       # View service logs
```

### **Utility Commands**
```bash
npm run install:all       # Install all dependencies
npm run dev               # Start both frontend and backend
```

## 📁 Project Structure

```
perplexity-clone/
├── package.json              # Root package.json with scripts
├── src/
│   ├── frontend/            # Next.js frontend
│   │   ├── package.json     # Frontend dependencies
│   │   └── src/             # Frontend source code
│   ├── api/                 # FastAPI backend
│   ├── core/                # Core utilities
│   └── middleware/          # Middleware system
├── docker-compose.yml       # Docker services
└── README.md                # Project documentation
```

## 🚀 Development Workflow

### **1. First Time Setup**
```bash
# Install all dependencies
npm run install:all

# Or install separately
npm run frontend:install
npm run backend:install
```

### **2. Daily Development**
```bash
# Start frontend (most common)
npm run frontend:dev

# Start backend if needed
npm run backend:dev

# Start both simultaneously
npm run dev
```

### **3. Production Testing**
```bash
# Build and start frontend
npm run frontend:build
npm run frontend:start

# Test with Docker
npm run docker:up
```

## 🌐 Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Next.js search interface |
| **Backend API** | http://localhost:8000 | FastAPI backend |
| **Grafana** | http://localhost:3001 | Monitoring dashboards |
| **Prometheus** | http://localhost:9090 | Metrics collection |

## 🔍 Troubleshooting

### **Frontend Won't Start**
```bash
# Check if you're in the right directory
pwd  # Should show: /path/to/perplexity-clone

# Install dependencies
npm run frontend:install

# Try starting again
npm run frontend:dev
```

### **Backend Won't Start**
```bash
# Check Python environment
python --version  # Should be 3.8+

# Install dependencies
npm run backend:install

# Try starting again
npm run backend:dev
```

### **Port Conflicts**
```bash
# Check what's using the ports
lsof -i :3000  # Frontend port
lsof -i :8000  # Backend port

# Kill conflicting processes
kill -9 <PID>
```

### **Docker Issues**
```bash
# Check Docker status
docker --version
docker-compose --version

# Restart Docker services
npm run docker:down
npm run docker:up
```

## 📱 What You'll See

### **Frontend (http://localhost:3000)**
- **Modern Search Interface** - Clean, professional design
- **Smart Search Bar** - Auto-complete and suggestions
- **Responsive Results** - Beautiful result cards
- **Professional UI** - Tailwind CSS styling

### **Backend (http://localhost:8000)**
- **Health Check** - `/health` endpoint
- **Metrics** - `/metrics` endpoint for Prometheus
- **API Documentation** - `/docs` for Swagger UI

### **Monitoring**
- **Grafana** - Beautiful dashboards
- **Prometheus** - Metrics collection
- **Health Checks** - Service status monitoring

## 🎯 Next Steps

1. **Start Frontend**: `npm run frontend:dev`
2. **Open Browser**: Navigate to http://localhost:3000
3. **Test Search**: Try the search interface
4. **Explore Features**: Check out the responsive design
5. **Start Backend**: `npm run backend:dev` (if needed)

## 🆘 Getting Help

- **Check Logs**: Look at terminal output for error messages
- **Verify Dependencies**: Ensure Node.js 18+ and Python 3.8+ are installed
- **Check Ports**: Make sure ports 3000, 8000, 3001, 9090 are available
- **Review Documentation**: Check README.md and other docs

---

**Your Perplexity clone is ready to run! 🚀**

Start with: `npm run frontend:dev`
