/**
 * API service for handling communication with the backend.
 * Centralizes API logic and environment configuration.
 */

export interface TextProcessRequest {
  text: string;
}

export interface TextProcessResponse {
  result: string;
}

export interface ApiError {
  message: string;
  status?: number;
}

class ApiService {
  private getApiUrl(): string {
    // Always use the local API route - it will handle proxying to the backend
    // This works both in development (with Next.js proxy) and production (with API route)
    return "/api/v1/process-text";
  }

  async processText(request: TextProcessRequest): Promise<TextProcessResponse> {
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
        throw new Error(`Failed to process text: ${error.message}`);
      }
      throw new Error("Failed to process text. Please try again.");
    }
  }
}

// Export singleton instance
export const apiService = new ApiService();
