// Mock Next.js server components before importing the route
jest.mock("next/server", () => ({
  NextRequest: class MockNextRequest {
    constructor(input, init = {}) {
      this.url = input;
      this.method = init.method || "GET";
      this.body = init.body || null;
      this.headers = {
        get: jest
          .fn()
          .mockReturnValue(
            init.headers?.["Content-Type"] || "application/json",
          ),
      };
      this.json = jest.fn().mockResolvedValue(JSON.parse(init.body || "{}"));
    }
  },
  NextResponse: class MockNextResponse {
    constructor(body, options = {}) {
      this.body = body;
      this.status = options.status || 200;
      this.headers = new Map();

      if (options.headers) {
        Object.entries(options.headers).forEach(([key, value]) => {
          this.headers.set(key, value);
        });
      }
    }

    static json(data, options = {}) {
      const response = new MockNextResponse(JSON.stringify(data), options);
      response.json = jest.fn().mockResolvedValue(data);
      return response;
    }
  },
}));

// Now import the route functions using ES6 import
import { POST, OPTIONS } from "../route";

// Mock fetch globally
global.fetch = jest.fn();

describe("/api/v1/search", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset environment variables
    delete process.env.NODE_ENV;
    delete process.env.BACKEND_SERVICE_URL;
  });

  describe("POST", () => {
    it("should successfully proxy search request to backend", async () => {
      // Mock successful backend response
      const mockBackendResponse = {
        ok: true,
        status: 200,
        json: jest
          .fn()
          .mockResolvedValue({ result: "You searched for: test query" }),
        headers: new Map([["content-type", "application/json"]]),
      };
      global.fetch.mockResolvedValue(mockBackendResponse);

      const request = {
        json: jest.fn().mockResolvedValue({ query: "test query" }),
        headers: {
          get: jest.fn().mockReturnValue("application/json"),
        },
      };

      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data).toEqual({ result: "You searched for: test query" });
      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/search",
        expect.objectContaining({
          method: "POST",
          headers: expect.objectContaining({
            "Content-Type": "application/json",
          }),
          body: JSON.stringify({ query: "test query" }),
        }),
      );
    });

    it("should use Docker service name when NODE_ENV is production", async () => {
      process.env.NODE_ENV = "production";
      process.env.BACKEND_SERVICE_URL = "http://backend:8000";

      const mockBackendResponse = {
        ok: true,
        status: 200,
        json: jest
          .fn()
          .mockResolvedValue({ result: "You searched for: docker query" }),
        headers: new Map([["content-type", "application/json"]]),
      };
      global.fetch.mockResolvedValue(mockBackendResponse);

      const request = {
        json: jest.fn().mockResolvedValue({ query: "docker query" }),
        headers: {
          get: jest.fn().mockReturnValue("application/json"),
        },
      };

      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data).toEqual({ result: "You searched for: docker query" });
      expect(global.fetch).toHaveBeenCalledWith(
        "http://backend:8000/api/v1/search",
        expect.any(Object),
      );
    });

    it("should handle backend error responses", async () => {
      const mockBackendResponse = {
        ok: false,
        status: 400,
        text: jest.fn().mockResolvedValue("Bad Request: Query cannot be empty"),
        headers: new Map([["content-type", "text/plain"]]),
      };
      global.fetch.mockResolvedValue(mockBackendResponse);

      const request = {
        json: jest.fn().mockResolvedValue({ query: "" }),
        headers: {
          get: jest.fn().mockReturnValue("application/json"),
        },
      };

      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data).toEqual({
        error: "Backend error: Bad Request: Query cannot be empty",
      });
    });

    it("should handle network errors gracefully", async () => {
      global.fetch.mockRejectedValue(new Error("Network error"));

      const request = {
        json: jest.fn().mockResolvedValue({ query: "test query" }),
        headers: {
          get: jest.fn().mockReturnValue("application/json"),
        },
      };

      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(500);
      expect(data).toEqual({
        error: "Failed to communicate with backend service",
        details: "Network error",
      });
    });

    it("should forward authorization headers when present", async () => {
      const mockBackendResponse = {
        ok: true,
        status: 200,
        json: jest
          .fn()
          .mockResolvedValue({ result: "You searched for: auth query" }),
        headers: new Map([["content-type", "application/json"]]),
      };
      global.fetch.mockResolvedValue(mockBackendResponse);

      const request = {
        json: jest.fn().mockResolvedValue({ query: "auth query" }),
        headers: {
          get: jest.fn().mockReturnValue("Bearer test-token"),
        },
      };

      const response = await POST(request);
      expect(response.status).toBe(200);

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/search",
        expect.objectContaining({
          headers: expect.objectContaining({
            authorization: "Bearer test-token",
          }),
        }),
      );
    });

    it("should handle malformed JSON gracefully", async () => {
      const request = {
        json: jest.fn().mockRejectedValue(new Error("Invalid JSON")),
        headers: {
          get: jest.fn().mockReturnValue("application/json"),
        },
      };

      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(500);
      expect(data.error).toContain(
        "Failed to communicate with backend service",
      );
    });
  });

  describe("OPTIONS", () => {
    it("should handle CORS preflight requests", async () => {
      const response = await OPTIONS();

      expect(response.status).toBe(200);
      expect(response.headers.get("Access-Control-Allow-Origin")).toBe("*");
      expect(response.headers.get("Access-Control-Allow-Methods")).toBe(
        "POST, OPTIONS",
      );
      expect(response.headers.get("Access-Control-Allow-Headers")).toBe(
        "Content-Type, Authorization",
      );
    });
  });
});
