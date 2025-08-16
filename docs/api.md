# API Documentation

This document contains the API endpoints for the Perplexity Clone application.

## Current Endpoints

### GET /api/v1/health

**Description:** Health check endpoint to verify API status and uptime.

**Request Body (Input):** None

**Success Response (Output):**
```json
{
  "status": "healthy",
  "message": "API is running",
  "timestamp": "2025-08-14T21:34:46.123456+00:00"
}
```

**Effects:** None, this is a pure status check.

**Requirements:** None.

### POST /api/v1/search

**Description:** Performs web search queries and returns relevant web sources.

**Request Body (Input):**
```json
{
  "query": "string"
}
```

**Success Response (Output):**
```json
{
  "sources": [
    {
      "title": "What is Artificial Intelligence?",
      "url": "https://example.com/ai-definition",
      "snippet": "Artificial Intelligence (AI) is a branch of computer science...",
      "source": "web_search"
    }
  ]
}
```

**Effects:** Performs live web search using Serper.dev API.

**Requirements:** Requires valid SERPER_API_KEY environment variable.

## API Models

### SearchRequest
```json
{
  "query": "string"
}
```

### WebSearchResult
```json
{
  "title": "string",
  "url": "string",
  "snippet": "string",
  "source": "string"
}
```

### SearchResponse
```json
{
  "sources": [
    {
      "title": "string",
      "url": "string",
      "snippet": "string",
      "source": "string"
    }
  ]
}
```

### HealthResponse
```json
{
  "status": "string",
  "message": "string",
  "timestamp": "string"
}
```

## Error Handling

The API returns standard HTTP status codes:

- **200 OK**: Successful request
- **400 Bad Request**: Invalid input (e.g., empty text)
- **500 Internal Server Error**: Server-side error

Error responses include a `detail` field with the error message:

```json
{
  "detail": "Search query cannot be empty"
}
```

## CORS Configuration

The API supports CORS with the following configuration:
- **Allowed Origins**: Configured via environment variables
- **Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS
- **Allowed Headers**: Content-Type, Authorization, and others
- **Credentials**: Supported
- **Max Age**: 24 hours for preflight responses

## Future Endpoints

The following endpoints are planned for future phases but are not yet implemented:

### Authentication Endpoints
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/profile` - Get user profile

### Search Endpoints
- `GET /api/v1/search/history` - Get search history
- `DELETE /api/v1/search/history/:id` - Delete search history item

### User Management Endpoints
- `POST /api/v1/users` - Create user account
- `PUT /api/v1/users/profile` - Update user profile
- `GET /api/v1/users/subscription` - Get subscription details
