import React from 'react';
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

  return (
    <div className="h-full flex flex-col">
      {/* Search Bar Section */}
      <div className="flex-1 flex items-center justify-center px-8">
        <div className="w-full max-w-3xl">
          <SearchHeader />
          
          {/* Search Input */}
          <div className="relative">
            <SearchInput onSearch={search} isLoading={isLoading} />
            <SearchSuggestions onSearch={search} isLoading={isLoading} />
          </div>
        </div>
      </div>

      {/* Result Display Area */}
      <ResultDisplay 
        isLoading={isLoading}
        result={result}
        error={error}
        hasSearched={hasSearched}
      />
    </div>
  );
}
