import { useState } from "react";
import {
  apiService,
  SearchRequest,
  WebSearchResult,
  ExtractedContent,
  LLMAnswer,
} from "../services/api";

interface ConversationEntry {
  query: string;
  sources: WebSearchResult[];
  extractedContent: ExtractedContent[];
  contentSummary?: string;
  llmAnswer?: LLMAnswer;
  originalQuery?: string;
  enhancedQuery?: string;
  queryEnhancementSuccess?: boolean;
  timestamp: Date;
}

interface SearchState {
  isLoading: boolean;
  sources: WebSearchResult[];
  extractedContent: ExtractedContent[];
  contentSummary?: string;
  llmAnswer?: LLMAnswer;
  error: string;
  hasSearched: boolean;
  currentQuery: string;
  originalQuery?: string;
  enhancedQuery?: string;
  queryEnhancementSuccess?: boolean;
  conversationHistory: ConversationEntry[];
}

interface UseSearchReturn extends SearchState {
  search: (query: string) => Promise<void>;
  clearResults: () => void;
  updateQuery: (query: string) => void;
}

/**
 * Custom hook for managing search functionality
 * Handles API communication, loading states, and error handling
 */
export function useSearch(): UseSearchReturn {
  const [isLoading, setIsLoading] = useState(false);
  const [sources, setSources] = useState<WebSearchResult[]>([]);
  const [extractedContent, setExtractedContent] = useState<ExtractedContent[]>(
    [],
  );
  const [contentSummary, setContentSummary] = useState<string>("");
  const [llmAnswer, setLlmAnswer] = useState<LLMAnswer | undefined>(undefined);
  const [error, setError] = useState("");
  const [hasSearched, setHasSearched] = useState(false);
  const [currentQuery, setCurrentQuery] = useState("");
  const [originalQuery, setOriginalQuery] = useState<string>("");
  const [enhancedQuery, setEnhancedQuery] = useState<string>("");
  const [queryEnhancementSuccess, setQueryEnhancementSuccess] = useState<
    boolean | undefined
  >(undefined);
  const [conversationHistory, setConversationHistory] = useState<
    ConversationEntry[]
  >([]);

  const search = async (query: string) => {
    if (!query.trim()) return;

    setIsLoading(true);
    setError("");
    setSources([]);
    setExtractedContent([]);
    setContentSummary("");
    setLlmAnswer(undefined);
    setHasSearched(true);
    setCurrentQuery(query.trim());

    try {
      const request: SearchRequest = { query };
      const data = await apiService.search(request);
      setSources(data.sources);
      setExtractedContent(data.extracted_content || []);
      setContentSummary(data.content_summary || "");
      setLlmAnswer(data.llm_answer);
      setOriginalQuery(data.original_query || "");
      setEnhancedQuery(data.enhanced_query || "");
      setQueryEnhancementSuccess(data.query_enhancement_success);

      // Add to conversation history
      const newEntry: ConversationEntry = {
        query: query.trim(),
        sources: data.sources,
        extractedContent: data.extracted_content || [],
        contentSummary: data.content_summary,
        llmAnswer: data.llm_answer,
        originalQuery: data.original_query,
        enhancedQuery: data.enhanced_query,
        queryEnhancementSuccess: data.query_enhancement_success,
        timestamp: new Date(),
      };

      setConversationHistory((prev) => [...prev, newEntry]);
    } catch (err) {
      console.error("Search error:", err);
      setError(
        err instanceof Error
          ? err.message
          : "Failed to process search. Please try again.",
      );
    } finally {
      setIsLoading(false);
    }
  };

  const clearResults = () => {
    setSources([]);
    setExtractedContent([]);
    setContentSummary("");
    setLlmAnswer(undefined);
    setError("");
    setHasSearched(false);
    setCurrentQuery("");
    setOriginalQuery("");
    setEnhancedQuery("");
    setQueryEnhancementSuccess(undefined);
    setConversationHistory([]);
  };

  const updateQuery = (query: string) => {
    setCurrentQuery(query);
  };

  return {
    isLoading,
    sources,
    extractedContent,
    contentSummary,
    llmAnswer,
    error,
    hasSearched,
    currentQuery,
    originalQuery,
    enhancedQuery,
    queryEnhancementSuccess,
    conversationHistory,
    search,
    clearResults,
    updateQuery,
  };
}
