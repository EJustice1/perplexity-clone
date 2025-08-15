import React from 'react';
import { SearchHeader, SearchInput, SearchSuggestions, ResultDisplay } from '../features';

/**
 * Main content area component containing the search interface
 * This will be the primary interaction point for users
 * Uses modular subcomponents for better organization and reusability
 */
export default function MainContent() {
  return (
    <div className="h-full flex flex-col">
      {/* Search Bar Section */}
      <div className="flex-1 flex items-center justify-center px-8">
        <div className="w-full max-w-3xl">
          <SearchHeader />
          
          {/* Search Input */}
          <div className="relative">
            <SearchInput disabled={true} />
            <SearchSuggestions disabled={true} />
          </div>
        </div>
      </div>

      {/* Result Display Area */}
      <ResultDisplay />
    </div>
  );
}
