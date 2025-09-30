/**
 * API service for handling communication with the backend.
 * Centralizes API logic and environment configuration.
 */

export interface SearchRequest {
  query: string;
}

export interface WebSearchResult {
  title: string;
  url: string;
  snippet: string;
  source: string;
}

export interface ExtractedContent {
  url: string;
  title: string;
  extracted_text: string;
  extraction_method: string;
  success: boolean;
  error_message?: string;
}

export interface LLMAnswer {
  answer: string;
  success: boolean;
  error_message?: string;
  tokens_used?: number;
}

export interface SearchResponse {
  sources: WebSearchResult[];
  extracted_content?: ExtractedContent[];
  content_summary?: string;
  llm_answer?: LLMAnswer;
  citations?: string[];
  sub_queries: string[];
  original_query?: string;
}

export interface ApiError {
  message: string;
  status?: number;
}

export interface TopicSubscriptionRequest {
  email: string;
  topic: string;
}

export interface TopicSubscriptionResponse {
  subscription_id: string;
  message: string;
}

class ApiService {
  private getSearchUrl(): string {
    // Always use the local API route - it will handle proxying to the backend
    // This works both in development (with Next.js proxy) and production (with API route)
    return "/api/v1/search";
  }

  private getSubscriptionUrl(): string {
    return "/api/v1/subscriptions";
  }

  async search(request: SearchRequest): Promise<SearchResponse> {
    const endpoint = this.getSearchUrl();

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`Failed to search: ${error.message}`);
      }
      throw new Error("Failed to search. Please try again.");
    }
  }

  async subscribeToTopic(
    request: TopicSubscriptionRequest,
  ): Promise<TopicSubscriptionResponse> {
    const endpoint = this.getSubscriptionUrl();

    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => null);
      const errorMessage =
        errorBody?.detail ?? `Subscription failed with status ${response.status}`;
      throw new Error(errorMessage);
    }

    return response.json();
  }
}

// Export singleton instance
export const apiService = new ApiService();
