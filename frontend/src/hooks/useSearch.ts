import { useState } from 'react';
import { apiService, SearchRequest, WebSearchResult, ExtractedContent } from '../services/api';

interface ConversationEntry {
  query: string;
  sources: WebSearchResult[];
  extractedContent: ExtractedContent[];
  contentSummary?: string;
  timestamp: Date;
}

interface SearchState {
  isLoading: boolean;
  sources: WebSearchResult[];
  extractedContent: ExtractedContent[];
  contentSummary?: string;
  error: string;
  hasSearched: boolean;
  currentQuery: string;
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
  const [extractedContent, setExtractedContent] = useState<ExtractedContent[]>([]);
  const [contentSummary, setContentSummary] = useState<string>('');
  const [error, setError] = useState('');
  const [hasSearched, setHasSearched] = useState(false);
  const [currentQuery, setCurrentQuery] = useState('');
  const [conversationHistory, setConversationHistory] = useState<ConversationEntry[]>([]);

  const search = async (query: string) => {
    if (!query.trim()) return;

    setIsLoading(true);
    setError('');
    setSources([]);
    setExtractedContent([]);
    setContentSummary('');
    setHasSearched(true);
    setCurrentQuery(query.trim());

    try {
      const request: SearchRequest = { query };
      const data = await apiService.search(request);
      setSources(data.sources);
      setExtractedContent(data.extracted_content || []);
      setContentSummary(data.content_summary || '');
      
      // Add to conversation history
      const newEntry: ConversationEntry = {
        query: query.trim(),
        sources: data.sources,
        extractedContent: data.extracted_content || [],
        contentSummary: data.content_summary,
        timestamp: new Date()
      };
      
      setConversationHistory(prev => [...prev, newEntry]);
    } catch (err) {
      console.error('Search error:', err);
      setError(err instanceof Error ? err.message : 'Failed to process search. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const clearResults = () => {
    setSources([]);
    setExtractedContent([]);
    setContentSummary('');
    setError('');
    setHasSearched(false);
    setCurrentQuery('');
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
    error,
    hasSearched,
    currentQuery,
    conversationHistory,
    search,
    clearResults,
    updateQuery,
  };
}
