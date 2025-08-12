# API Endpoints Documentation

This document contains the current API endpoints for the Interactive Search Engine project.

## Current Endpoints (Stage 0)

### Health Check

**Endpoint:** `GET /health`

**Description:** Verifies that the API is running and healthy.

**Request Body (Input):** None

**Success Response (Output):**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

**Effects:** None, this is a pure health check endpoint.

**Requirements:** None

## Future Endpoints (Not Yet Implemented)

*Note: These endpoints will be implemented in future stages according to the project plan.*

- `POST /api/v1/process-text` - Core text processing feature (Stage 1)
- Authentication endpoints (Future stages)
- User management endpoints (Future stages)
