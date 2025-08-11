# Infrastructure

Infrastructure as Code and deployment configurations for the Perplexity Clone application.

## Directory Structure

```
infrastructure/
├── docker/           # Docker Compose and orchestration
├── monitoring/       # Prometheus, Grafana configurations
├── terraform/        # Infrastructure as Code
└── README.md         # This file
```

## Docker

### Local Development

```bash
# Start all services
cd infrastructure/docker
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Services

- **Backend**: FastAPI application on port 8000
- **Frontend**: Next.js application on port 3000
- **Prometheus**: Metrics collection on port 9090
- **Grafana**: Monitoring dashboard on port 3001

## Monitoring

### Prometheus

- **Port**: 9090
- **Metrics**: HTTP request metrics, application health
- **Retention**: 15 days
- **Scraping**: Every 15 seconds

### Grafana

- **Port**: 3001
- **Default Credentials**: admin/admin
- **Dashboards**: Application metrics, system health
- **Data Sources**: Prometheus

### Setup

```bash
# Install monitoring stack
cd infrastructure/monitoring
./setup-monitoring.sh

# Access Grafana
open http://localhost:3001
```

## Terraform

### Prerequisites

- Terraform >= 1.0
- AWS CLI configured
- Appropriate AWS permissions

### Usage

```bash
cd infrastructure/terraform

# Initialize
terraform init

# Plan changes
terraform plan

# Apply changes
terraform apply

# Destroy infrastructure
terraform destroy
```

### Infrastructure Components

- **VPC**: Network isolation and security
- **ECS**: Container orchestration
- **RDS**: Database services
- **ALB**: Load balancing
- **CloudWatch**: Logging and monitoring

## Environment Variables

### Backend

```bash
SERVICE_NAME=backend
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=production
ENABLE_METRICS=true
```

### Frontend

```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NODE_ENV=production
```

### Monitoring

```bash
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
```

## Deployment

### Backend Deployment

```bash
# Build image
docker build -t perplexity-backend backend/

# Push to registry
docker tag perplexity-backend your-registry/perplexity-backend:latest
docker push your-registry/perplexity-backend:latest

# Deploy to ECS
aws ecs update-service --cluster perplexity-cluster --service backend-service --force-new-deployment
```

### Frontend Deployment

```bash
# Build image
docker build -t perplexity-frontend frontend/

# Push to registry
docker tag perplexity-frontend your-registry/perplexity-frontend:latest
docker push your-registry/perplexity-frontend:latest

# Deploy to ECS
aws ecs update-service --cluster perplexity-cluster --service frontend-service --force-new-deployment
```

## Security

### Network Security

- VPC with private subnets
- Security groups limiting access
- WAF for web application protection
- SSL/TLS termination at load balancer

### Access Control

- IAM roles with least privilege
- Secrets management via AWS Secrets Manager
- Container security scanning
- Regular security updates

## Monitoring and Alerting

### Metrics

- Application performance metrics
- Infrastructure health metrics
- Business metrics
- Custom application metrics

### Alerts

- High error rates
- High latency
- Service unavailability
- Resource utilization

### Dashboards

- Application overview
- Infrastructure health
- Business metrics
- Custom operational dashboards

## Troubleshooting

### Common Issues

1. **Container won't start**
   - Check logs: `docker logs <container-id>`
   - Verify environment variables
   - Check resource limits

2. **Metrics not appearing**
   - Verify Prometheus configuration
   - Check service discovery
   - Validate metrics endpoints

3. **High resource usage**
   - Monitor container metrics
   - Check application logs
   - Review resource limits

### Getting Help

- Check application logs
- Review infrastructure logs
- Monitor metrics and alerts
- Review security group rules
