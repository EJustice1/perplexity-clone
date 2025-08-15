import React, { useState } from 'react';
import { SearchHeader, SearchInput, SearchSuggestions, ResultDisplay } from '../features';
import { useSearch } from '../../hooks';

/**
 * Main content area component containing the search interface
 * This will be the primary interaction point for users
 * Uses modular subcomponents for better organization and reusability
 * Now manages search state and API communication via custom hook
 */
export default function MainContent() {
  const { isLoading, result, error, hasSearched, search } = useSearch();
  const [currentQuery, setCurrentQuery] = useState('');

  const handleSearch = (query: string) => {
    setCurrentQuery(query);
    search(query);
  };

  const handleRecommendationClick = (query: string) => {
    setCurrentQuery(query);
    // Auto-submit the search after a short delay to show the query in the input
    setTimeout(() => {
      search(query);
    }, 100);
  };

  return (
    <div className="min-h-full flex flex-col bg-gray-50">
      {/* Search Bar Section - Centered and responsive */}
      <div className="flex-1 flex items-center justify-center px-4 lg:px-8 py-8 lg:py-16">
        <div className="w-full max-w-3xl mx-auto">
          <SearchHeader />
          
          {/* Search Input with proper spacing */}
          <div className="relative mt-6">
            <SearchInput 
              onSearch={handleSearch} 
              isLoading={isLoading} 
              externalQuery={currentQuery}
            />
            <SearchSuggestions 
              onSearch={handleRecommendationClick} 
              isLoading={isLoading} 
            />
          </div>
        </div>
      </div>

      {/* Result Display Area - Proper spacing and responsive */}
      <div className="flex-shrink-0">
        <ResultDisplay 
          isLoading={isLoading}
          result={result}
          error={error}
          hasSearched={hasSearched}
        />
      </div>
    </div>
  );
}
