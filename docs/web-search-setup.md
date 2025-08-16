# Web Search Setup Guide

This document explains how to set up and use the web search functionality in the Perplexity Clone application.

## Overview

The application now includes a web search feature that allows users to search the live web and get relevant results. The implementation uses an implementation-agnostic interface, currently implemented with Serper.dev as the search provider.

## Architecture

### Implementation-Agnostic Interface

The web search system is designed with a clean abstraction layer:

- **`WebSearchProvider`**: Abstract interface that defines the contract for web search providers
- **`SerperWebSearchProvider`**: Concrete implementation using Serper.dev API
- **`WebSearchService`**: Service wrapper that uses the provider pattern

This design allows easy switching between different search providers in the future without changing the application logic.

### Current Implementation

- **Provider**: Serper.dev (Google search results)
- **API Endpoint**: `https://google.serper.dev/search`
- **Authentication**: API key via `X-API-KEY` header

## Setup Instructions

### 1. Get Serper.dev API Key

1. Visit [https://serper.dev/](https://serper.dev/)
2. Sign up for an account
3. Get your API key from the dashboard
4. Note: Serper.dev offers free tier with limited requests

### 2. Local Development Setup

1. **Create environment file**:
   ```bash
   cd backend
   cp env.example .env
   ```

2. **Add your API key**:
   ```bash
   # In backend/.env
   SERPER_API_KEY=your_actual_api_key_here
   ```

3. **Update docker-compose.yml** (already done):
   The docker-compose.yml file is already configured to use the `SERPER_API_KEY` environment variable.

4. **Start the application**:
   ```bash
   docker-compose up --build
   ```

### 3. Production Setup

For production deployment, the API key should be stored in Google Secret Manager:

1. **Create secret in Google Secret Manager**:
   ```bash
   gcloud secrets create serper-api-key --data-file=<(echo -n "your_api_key_here")
   ```

2. **Grant access to Cloud Run service account**:
   ```bash
   gcloud secrets add-iam-policy-binding serper-api-key \
     --member="serviceAccount:your-service-account@your-project.iam.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor"
   ```

3. **Update Terraform configuration** (when ready for production):
   Add the secret to your Cloud Run service configuration.

## Usage

### API Endpoint

**POST** `/api/v1/search`

**Request**:
```json
{
  "query": "What is artificial intelligence?"
}
```

**Response**:
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

### Frontend Integration

The frontend automatically displays web search results in a clean, organized format:

- Each result shows the title, URL, and snippet
- Titles are clickable links that open in new tabs
- Results are displayed in cards with hover effects
- Responsive design for mobile and desktop

## Testing

### Backend Tests

Run the web search service tests:

```bash
cd backend
pytest tests/test_web_search.py -v
```

### Frontend Tests

Run the frontend tests:

```bash
cd frontend
npm test
```

## Configuration Options

### Environment Variables

- **`SERPER_API_KEY`**: Required. Your Serper.dev API key
- **`CORS_ORIGINS`**: Optional. CORS configuration for frontend domains

### Search Parameters

- **`max_results`**: Maximum number of search results (default: 5, max: 10)
- **`query`**: Search query string (required)

## Error Handling

The system handles various error scenarios:

- **Missing API key**: Clear error message about required configuration
- **API failures**: Graceful fallback with user-friendly error messages
- **Network issues**: Timeout handling and retry logic
- **Invalid queries**: Input validation and error reporting

## Future Enhancements

The implementation-agnostic design supports future enhancements:

1. **Additional Providers**: Easy to add Google Custom Search, Brave Search, etc.
2. **Provider Selection**: Could allow users to choose their preferred search engine
3. **Caching**: Implement result caching to reduce API calls
4. **Rate Limiting**: Add rate limiting to prevent API abuse
5. **Fallback Providers**: Automatic fallback if primary provider fails

## Troubleshooting

### Common Issues

1. **"SERPER_API_KEY environment variable is required"**
   - Ensure you've created a `.env` file in the backend directory
   - Verify the API key is correctly set
   - Restart the Docker containers after adding the environment variable

2. **"Web search failed with status 401"**
   - Check that your Serper.dev API key is valid
   - Verify you haven't exceeded your API quota
   - Ensure the API key is correctly formatted

3. **"Web search request failed"**
   - Check your internet connection
   - Verify the Serper.dev service is available
   - Check Docker container logs for more details

### Debug Mode

To enable debug logging, set the log level in your environment:

```bash
LOG_LEVEL=DEBUG
```

## Support

For issues related to:

- **Serper.dev API**: Contact [Serper.dev support](https://serper.dev/)
- **Application integration**: Check the application logs and test suite
- **Configuration**: Verify environment variables and Docker setup
