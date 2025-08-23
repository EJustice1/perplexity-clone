# API Documentation

This document describes the backend API endpoints for the search engine system.

## Base URL

All API endpoints are prefixed with `/api/v1`.

## Endpoints

### Health Check

**Endpoint:** `GET /api/v1/health`

**Description:** Check the health status of the API.

**Request Body:** None

**Success Response (200 OK):**
```json
{
  "status": "healthy",
  "message": "API is running",
  "timestamp": "2025-01-27T10:30:00.123456"
}
```

**Effects:** None, this is a pure health check endpoint.

**Requirements:** None

---

### Search

**Endpoint:** `POST /api/v1/search`

**Description:** Process a search query, perform web search, and extract content from discovered web pages.

**Request Body:**
```json
{
  "query": "What is artificial intelligence?"
}
```

**Success Response (200 OK):**
```json
{
  "sources": [
    {
      "title": "What is Artificial Intelligence?",
      "url": "https://example.com/ai-definition",
      "snippet": "Artificial Intelligence (AI) is a branch of computer science...",
      "source": "web_search"
    }
  ],
  "extracted_content": [
    {
      "url": "https://example.com/ai-definition",
      "title": "What is Artificial Intelligence?",
      "extracted_text": "Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines that work and react like humans. Some of the activities computers with artificial intelligence are designed for include speech recognition, learning, planning, and problem solving...",
      "extraction_method": "trafilatura",
      "success": true,
      "error_message": null
    }
  ],
  "content_summary": "Successfully extracted content from 1 out of 1 sources."
}
```

**Effects:** 
- Performs web search using configured search provider (Serper)
- Fetches HTML content from top 3 search results
- Extracts and cleans textual content using trafilatura (primary) and BeautifulSoup (fallback)
- Returns both search results and extracted content for verification

**Requirements:** 
- Valid search query (non-empty string)
- SERPER_API_KEY environment variable configured
- Internet access for web search and content fetching

---

## Data Models

### SearchRequest
```typescript
interface SearchRequest {
  query: string;  // The search query to be processed
}
```

### WebSearchResult
```typescript
interface WebSearchResult {
  title: string;      // Title of the search result
  url: string;        // URL of the search result
  snippet: string;    // Snippet/description of the search result
  source: string;     // Source of the search result (default: "web_search")
}
```

### ExtractedContent
```typescript
interface ExtractedContent {
  url: string;                    // URL of the source page
  title: string;                  // Title of the page
  extracted_text: string;         // Extracted and cleaned text content
  extraction_method: string;      // Method used for content extraction
  success: boolean;               // Whether content extraction was successful
  error_message?: string;         // Error message if extraction failed
}
```

### SearchResponse
```typescript
interface SearchResponse {
  sources: WebSearchResult[];           // List of web search results
  extracted_content: ExtractedContent[]; // List of extracted content from web pages
  content_summary?: string;             // Summary of extracted content for verification
}
```

### HealthResponse
```typescript
interface HealthResponse {
  status: string;    // Health status of the API
  message: string;   // Status message
  timestamp: string; // ISO timestamp of the health check
}
```

## Error Handling

### 400 Bad Request
Returned when the search query is empty or invalid.

```json
{
  "detail": "Search query cannot be empty"
}
```

### 500 Internal Server Error
Returned when an unexpected error occurs during processing.

```json
{
  "detail": "Internal server error"
}
```

## Content Extraction Methods

The system uses two methods for extracting content from web pages:

1. **Trafilatura (Primary)**: Advanced content extraction library that excels at extracting main article text while removing ads, navigation, and other boilerplate.

2. **BeautifulSoup (Fallback)**: Used when trafilatura fails, provides basic HTML parsing and text extraction.

## Performance Considerations

- Content extraction is limited to the top 3 search results for performance
- Concurrent requests are limited to 2 at a time to avoid overwhelming target servers
- Extracted content is truncated to 50,000 characters maximum
- Timeout is set to 30 seconds per URL to ensure responsiveness

## Future Enhancements

- **Stage 4**: LLM integration for answer synthesis using extracted content
- **Caching**: Content caching to avoid re-extracting from the same URLs
- **Rate Limiting**: Advanced rate limiting to respect target website policies
- **Multiple Providers**: Support for additional content extraction strategies
