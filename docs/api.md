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
  "content_summary": "Successfully extracted content from 1 out of 1 sources.",
  "llm_answer": {
    "answer": "Artificial Intelligence (AI) is a branch of computer science that focuses on creating intelligent machines capable of performing tasks that typically require human intelligence. Based on the extracted content, AI systems are designed to handle activities such as speech recognition, learning, planning, and problem solving.",
    "success": true,
    "error_message": null,
    "tokens_used": 67
  }
}
```

**Effects:** 
- Performs web search using configured search provider (Serper)
- Fetches HTML content from top 3 search results
- Extracts and cleans textual content using trafilatura (primary) and BeautifulSoup (fallback)
- Generates AI-powered answer using LLM based on extracted content (Retrieval-Augmented Generation)
- Returns synthesized answer, search results, and extracted content

**Requirements:** 
- Valid search query (non-empty string)
- SERPER_API_KEY environment variable configured
- LLM_API_KEY environment variable configured (for answer synthesis)
- Internet access for web search and content fetching
- **Stage Notes:** Stage 1 installed LangChain dependencies; Stage 2 adds adaptive query decomposition (1–5 sub-queries); Stage 3 aggregates multi-sub-query search metadata; Stage 4 collates extracted documents for internal context; Stage 5 synthesizes grounded answers; Stage 6 wires the full LangChain pipeline into `/api/v1/search` and returns answers with citations while preserving legacy fields.

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

### LLMAnswer
```typescript
interface LLMAnswer {
  answer: string;           // Synthesized answer from LLM
  success: boolean;         // Whether LLM synthesis was successful
  error_message?: string;   // Error message if LLM synthesis failed
  tokens_used?: number;     // Number of tokens used in LLM generation
}
```

### SearchResponse
```typescript
interface SearchResponse {
  sources: WebSearchResult[];           // List of web search results
  extracted_content: ExtractedContent[]; // List of extracted content from web pages
  content_summary?: string;             // Summary of extracted content for verification
  llm_answer?: LLMAnswer;              // AI-generated answer based on extracted content
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

- **Caching**: Content caching to avoid re-extracting from the same URLs
- **Rate Limiting**: Advanced rate limiting to respect target website policies
- **Multiple Providers**: Support for additional content extraction strategies
- **Advanced LLM Features**: Support for multiple LLM providers, conversation memory, and fine-tuning
