import { useState } from 'react';
import { apiService, SearchRequest, WebSearchResult } from '../services/api';

interface SearchState {
  isLoading: boolean;
  sources: WebSearchResult[];
  error: string;
  hasSearched: boolean;
  currentQuery: string;
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
  const [error, setError] = useState('');
  const [hasSearched, setHasSearched] = useState(false);
  const [currentQuery, setCurrentQuery] = useState('');

  const search = async (query: string) => {
    if (!query.trim()) return;

    setIsLoading(true);
    setError('');
    setSources([]);
    setHasSearched(true);
    setCurrentQuery(query.trim());

    try {
      const request: SearchRequest = { query };
      const data = await apiService.search(request);
      setSources(data.sources);
    } catch (err) {
      console.error('Search error:', err);
      setError(err instanceof Error ? err.message : 'Failed to process search. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const clearResults = () => {
    setSources([]);
    setError('');
    setHasSearched(false);
    setCurrentQuery('');
  };

  const updateQuery = (query: string) => {
    setCurrentQuery(query);
  };

  return {
    isLoading,
    sources,
    error,
    hasSearched,
    currentQuery,
    search,
    clearResults,
    updateQuery,
  };
}
