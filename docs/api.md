# API Endpoints Documentation

This document contains the current API endpoints for the Interactive Search Engine project.

## Current Endpoints (Stage 1)

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

### Text Processing

**Endpoint:** `POST /api/v1/process-text`

**Description:** Core feature endpoint that processes text by adding exclamation points around the input.

**Request Body (Input):**
```json
{
  "text": "some user input"
}
```

**Success Response (Output):**
```json
{
  "result": "!!! some user input !!!"
}
```

**Effects:** None, this is a pure data transformation endpoint.

**Requirements:** None

**Error Responses:**
- `400 Bad Request`: When the text field is empty or contains only whitespace

## Future Endpoints (Not Yet Implemented)

*Note: These endpoints will be implemented in future stages according to the project plan.*

- Authentication endpoints (Future stages)
- User management endpoints (Future stages)
- Search and content processing endpoints (Future stages)
