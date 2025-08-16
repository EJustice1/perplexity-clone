import React, { useState } from 'react';
import { useSearch } from '../../hooks';
import { SearchInput, SearchSuggestions, ResultDisplay } from '../features';

/**
 * Main content component that manages search functionality
 * Includes search input, suggestions, and results display
 * Supports both light and dark themes
 */
export default function MainContent() {
  const { isLoading, sources, error, hasSearched, search } = useSearch();
  const [currentQuery, setCurrentQuery] = useState('');

  const handleSearch = (query: string) => {
    setCurrentQuery(query);
    search(query);
  };

  const handleRecommendationClick = (query: string) => {
    setCurrentQuery(query);
    // Small delay to ensure the input updates before searching
    setTimeout(() => {
      search(query);
    }, 100);
  };

  return (
    <div className="min-h-full flex flex-col bg-gray-50 dark:bg-gray-900">
      <SearchInput 
        onSearch={handleSearch} 
        isLoading={isLoading} 
        externalQuery={currentQuery} 
      />
      <SearchSuggestions 
        onSearch={handleRecommendationClick} 
        isLoading={isLoading} 
      />
      <ResultDisplay 
        isLoading={isLoading}
        sources={sources}
        error={error}
        hasSearched={hasSearched}
      />
    </div>
  );
}
