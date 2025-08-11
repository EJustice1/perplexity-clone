# 📊 Monitoring Stack Documentation

## Overview

Your Perplexity Clone application now includes a complete monitoring stack with:
- **Prometheus** - Metrics collection and storage
- **Grafana** - Metrics visualization and dashboards
- **Application Metrics** - HTTP request counters, latency, and health monitoring

## 🚀 Quick Start

### 1. Start the Monitoring Stack

```bash
# Start everything (including monitoring)
docker-compose up --build -d

# Or start just monitoring services
docker-compose up prometheus grafana -d
```

### 2. Access Your Monitoring Tools

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5001

## 📈 What's Being Monitored

### Application Metrics
- **HTTP Request Count**: Total requests by method, endpoint, and status
- **Request Latency**: Response time histograms (50th and 95th percentiles)
- **Service Health**: Up/down status of all services

### Infrastructure Metrics
- **Container Health**: Docker container status and resource usage
- **Service Discovery**: Automatic detection of backend and frontend services

## 🔧 Using Prometheus

### View Targets
- Go to http://localhost:9090/targets
- Verify all services show "UP" status

### Query Metrics
- Go to http://localhost:9090/graph
- Use these example queries:

```promql
# Total HTTP requests
http_requests_total

# Request rate (requests per second)
rate(http_requests_total[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate (5xx responses)
rate(http_requests_total{status=~"5.."}[5m])
```

### View Raw Metrics
- Backend: http://localhost:8000/metrics
- Frontend: http://localhost:5001/metrics

## 🎨 Using Grafana

### 1. Login
- URL: http://localhost:3000
- Username: `admin`
- Password: `admin`

### 2. Import Dashboard
1. Click the "+" icon → "Import"
2. Copy the content from `grafana/dashboards/app-metrics.json`
3. Click "Load"
4. Select "Prometheus" as the data source
5. Click "Import"

### 3. Pre-built Dashboard Includes
- **HTTP Request Rate** - Requests per second by endpoint
- **Request Latency** - 95th and 50th percentile response times
- **Error Rates** - 5xx status codes
- **Service Health** - Up/down status of all services

## 🧪 Testing the Monitoring Stack

### Run the Test Script
```bash
./test-monitoring.sh
```

This script will:
- ✅ Check all services are responding
- ✅ Verify metrics endpoints are working
- ✅ Confirm Prometheus targets are healthy
- ✅ Generate test traffic
- ✅ Validate metrics collection

### Manual Testing
```bash
# Generate some traffic
for i in {1..10}; do
  curl http://localhost:8000/ > /dev/null
  curl http://localhost:5001/ > /dev/null
  sleep 1
done

# Check metrics in Prometheus
curl "http://localhost:9090/api/v1/query?query=http_requests_total"
```

## 📊 Available Metrics

### HTTP Metrics
- `http_requests_total` - Total request count
- `http_request_duration_seconds` - Request latency histogram

### Python Runtime Metrics
- `python_gc_objects_collected_total` - Garbage collection stats
- `python_info` - Python version information

### System Metrics
- `process_cpu_seconds_total` - CPU usage
- `process_resident_memory_bytes` - Memory usage

## 🚨 Alerts (Optional)

Prometheus includes pre-configured alerts for:
- **Service Down** - Critical alerts for backend/frontend failures
- **High Latency** - Warning when 95th percentile > 1 second
- **High Error Rate** - Warning when errors > 10%
- **High Request Rate** - Info when requests > 100/sec

## 🔍 Troubleshooting

### Prometheus Not Scraping
1. Check targets at http://localhost:9090/targets
2. Verify services are healthy
3. Check container logs: `docker-compose logs prometheus`

### Grafana Can't Connect to Prometheus
1. Verify Prometheus is running: `docker-compose ps prometheus`
2. Check network connectivity between containers
3. Verify data source configuration in Grafana

### No Metrics Appearing
1. Check if metrics endpoints are working: `curl http://localhost:8000/metrics`
2. Verify Prometheus configuration in `prometheus.yml`
3. Check container logs for errors

### Common Issues
- **Port conflicts**: Ensure ports 8000, 5001, 9090, 3000 are available
- **Permission issues**: Check Docker volume permissions
- **Memory limits**: Increase Docker memory allocation if needed

## 📚 Advanced Configuration

### Custom Metrics
Add custom metrics to your applications:

```python
from prometheus_client import Counter, Histogram, Gauge

# Custom business metrics
USER_LOGINS = Counter('user_logins_total', 'Total user logins')
ACTIVE_USERS = Gauge('active_users', 'Number of active users')
QUERY_DURATION = Histogram('query_duration_seconds', 'Query execution time')
```

### Alerting Rules
Modify `prometheus/alerts.yml` to add custom alerts:

```yaml
- alert: CustomAlert
  expr: your_metric > threshold
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Custom alert description"
```

### Grafana Dashboards
Create custom dashboards:
1. Design in Grafana UI
2. Export as JSON
3. Save to `grafana/dashboards/`
4. Restart Grafana container

## 🎯 Next Steps

1. **Import the dashboard** into Grafana
2. **Customize metrics** for your specific use case
3. **Set up alerts** for critical thresholds
4. **Add business metrics** relevant to your application
5. **Configure retention policies** for long-term storage

## 📞 Support

If you encounter issues:
1. Check the logs: `docker-compose logs [service-name]`
2. Verify configuration files
3. Run the test script: `./test-monitoring.sh`
4. Check service health endpoints

Your monitoring stack is production-ready and follows industry best practices! 🚀
