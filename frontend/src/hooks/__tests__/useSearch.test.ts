import { renderHook, act, waitFor } from "@testing-library/react";
import { useSearch } from "../useSearch";
import { apiService, WebSearchResult, SearchResponse } from "../../services/api";

// Mock the API service
jest.mock("../../services/api", () => ({
  apiService: {
    search: jest.fn(),
  },
}));

const mockApiService = apiService as jest.Mocked<typeof apiService>;

describe("useSearch", () => {
  const consoleErrorSpy = jest.spyOn(console, "error").mockImplementation(() => {});

  beforeEach(() => {
    jest.clearAllMocks();
    consoleErrorSpy.mockClear();
  });

  afterAll(() => {
    consoleErrorSpy.mockRestore();
  });

  it("should initialize with default state", () => {
    const { result } = renderHook(() => useSearch());

    expect(result.current.isLoading).toBe(false);
    expect(result.current.sources).toEqual([]);
    expect(result.current.error).toBe("");
    expect(result.current.hasSearched).toBe(false);
    expect(result.current.currentQuery).toBe("");
  });

  it("should handle empty query gracefully", async () => {
    const { result } = renderHook(() => useSearch());

    await act(async () => {
      await result.current.search("");
    });

    expect(result.current.isLoading).toBe(false);
    expect(result.current.sources).toEqual([]);
    expect(result.current.error).toBe("");
    expect(result.current.hasSearched).toBe(false);
    expect(result.current.currentQuery).toBe("");
    expect(result.current.subQueries).toEqual([]);
  });

  it("should handle whitespace-only query gracefully", async () => {
    const { result } = renderHook(() => useSearch());

    await act(async () => {
      await result.current.search("   ");
    });

    expect(result.current.isLoading).toBe(false);
    expect(result.current.sources).toEqual([]);
    expect(result.current.error).toBe("");
    expect(result.current.hasSearched).toBe(false);
    expect(result.current.currentQuery).toBe("");
    expect(result.current.subQueries).toEqual([]);
  });

  it("should handle API errors gracefully", async () => {
    const apiError = new Error("API Error");
    mockApiService.search.mockRejectedValue(apiError);

    const { result } = renderHook(() => useSearch());

    await act(async () => {
      await result.current.search("test query");
    });

    expect(result.current.isLoading).toBe(false);
    expect(result.current.sources).toEqual([]);
    expect(result.current.error).toBe("API Error");
    expect(result.current.hasSearched).toBe(true);
  });

  it("should handle unknown errors gracefully", async () => {
    // Mock API service to throw an unknown error
    mockApiService.search.mockRejectedValue("Unknown error" as never);

    const { result } = renderHook(() => useSearch());

    await act(async () => {
      await result.current.search("test query");
    });

    expect(result.current.isLoading).toBe(false);
    expect(result.current.sources).toEqual([]);
    expect(result.current.error).toBe(
      "Failed to process search. Please try again.",
    );
    expect(result.current.hasSearched).toBe(true);
  });

  it("should set loading state during search", async () => {
    let resolvePromise: (value: SearchResponse) => void;
    const promise = new Promise<SearchResponse>((resolve) => {
      resolvePromise = resolve;
    });
    mockApiService.search.mockReturnValue(promise);

    const { result } = renderHook(() => useSearch());

    act(() => {
      result.current.search("test query");
    });

    expect(result.current.isLoading).toBe(true);
    expect(result.current.hasSearched).toBe(true);

    // Resolve the promise
    resolvePromise!({
      sources: [],
      sub_queries: [],
      citations: [],
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
  });

  it("should clear results when clearResults is called", async () => {
    const mockResponse = {
      sources: [
        {
          title: "Test Result",
          url: "https://example.com",
          snippet: "Test snippet",
          source: "web_search",
        },
      ],
      sub_queries: ["test query"],
      citations: ["https://example.com"],
    };
    mockApiService.search.mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useSearch());

    // First, perform a search
    await act(async () => {
      await result.current.search("test query");
    });

    expect(result.current.sources).toEqual(mockResponse.sources);
    expect(result.current.hasSearched).toBe(true);
    expect(result.current.currentQuery).toBe("test query");

    // Then clear results
    act(() => {
      result.current.clearResults();
    });

    expect(result.current.sources).toEqual([]);
    expect(result.current.error).toBe("");
    expect(result.current.hasSearched).toBe(false);
    expect(result.current.currentQuery).toBe("");
    expect(result.current.subQueries).toEqual([]);
  });

  it("should update query when updateQuery is called", () => {
    const { result } = renderHook(() => useSearch());

    act(() => {
      result.current.updateQuery("new query");
    });

    expect(result.current.currentQuery).toBe("new query");
  });

  it("should clear error when starting a new search", async () => {
    // First, cause an error
    mockApiService.search.mockRejectedValue(new Error("First error"));

    const { result } = renderHook(() => useSearch());

    await act(async () => {
      await result.current.search("first query");
    });

    expect(result.current.error).toBe("First error");

    // Then, perform a successful search
    mockApiService.search.mockResolvedValue({
      sources: [
        {
          title: "Second Query Result",
          url: "https://example.com",
          snippet: "Second query snippet",
          source: "web_search",
        },
      ],
      sub_queries: ["second query"],
      citations: ["https://example.com"],
    });

    await act(async () => {
      await result.current.search("second query");
    });

    expect(result.current.error).toBe("");
    expect(result.current.sources).toHaveLength(1);
    expect(result.current.sources[0].title).toBe("Second Query Result");
  });

  it("should handle multiple rapid searches", async () => {
    const mockResponse = {
      sources: [
        {
          title: "Rapid Query Result",
          url: "https://example.com",
          snippet: "Rapid query snippet",
          source: "web_search",
        },
      ],
      sub_queries: ["query 3"],
      citations: ["https://example.com"],
    };
    mockApiService.search.mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useSearch());

    // Perform multiple rapid searches
    await act(async () => {
      await Promise.all([
        result.current.search("query 1"),
        result.current.search("query 2"),
        result.current.search("query 3"),
      ]);
    });

    // Should have processed the last search
    expect(result.current.sources).toEqual(mockResponse.sources);
    expect(mockApiService.search).toHaveBeenCalledTimes(3);
  });
});
