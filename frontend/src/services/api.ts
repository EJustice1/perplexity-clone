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
  private getApiUrl(): string {
    // Always use the local API route - it will handle proxying to the backend
    // This works both in development (with Next.js proxy) and production (with API route)
    return "/api/v1/search";
  }

  async search(request: SearchRequest): Promise<SearchResponse> {
    const endpoint = this.getApiUrl();

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
    console.log("Submitting topic subscription (placeholder)", request);

    await new Promise((resolve) => setTimeout(resolve, 400));

    const subscriptionId =
      typeof crypto !== "undefined" && "randomUUID" in crypto
        ? crypto.randomUUID()
        : `placeholder-${Date.now()}`;

    return {
      subscription_id: subscriptionId,
      message:
        "Subscription saved (placeholder). Backend persistence will be wired soon.",
    };
  }
}

// Export singleton instance
export const apiService = new ApiService();
