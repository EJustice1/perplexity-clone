import { useState } from 'react';
import { apiService, SearchRequest } from '../services/api';

interface SearchState {
  isLoading: boolean;
  result: string;
  error: string;
  hasSearched: boolean;
}

interface UseSearchReturn extends SearchState {
  search: (query: string) => Promise<void>;
  clearResults: () => void;
}

/**
 * Custom hook for managing search functionality
 * Handles API communication, loading states, and error handling
 */
export function useSearch(): UseSearchReturn {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState('');
  const [error, setError] = useState('');
  const [hasSearched, setHasSearched] = useState(false);

  const search = async (query: string) => {
    if (!query.trim()) return;

    setIsLoading(true);
    setError('');
    setResult('');
    setHasSearched(true);

    try {
      const request: SearchRequest = { query };
      const data = await apiService.search(request);
      setResult(data.result);
    } catch (err) {
      console.error('Search error:', err);
      setError(err instanceof Error ? err.message : 'Failed to process search. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const clearResults = () => {
    setResult('');
    setError('');
    setHasSearched(false);
  };

  return {
    isLoading,
    result,
    error,
    hasSearched,
    search,
    clearResults,
  };
}
