import React, { useState, useEffect } from 'react';

interface SearchInputProps {
  onSearch: (query: string) => void;
  isLoading?: boolean;
  externalQuery?: string;
}

/**
 * SearchInput component for the main search interface
 * Now interactive with search functionality and external query updates
 */
export default function SearchInput({ onSearch, isLoading = false, externalQuery }: SearchInputProps) {
  const [query, setQuery] = useState('');

  // Update internal query when external query changes
  useEffect(() => {
    if (externalQuery && externalQuery !== query) {
      setQuery(externalQuery);
    }
  }, [externalQuery, query]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSearch(query.trim());
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as unknown as React.FormEvent);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything..."
          className="w-full px-6 py-4 text-lg border border-gray-300 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all shadow-sm hover:shadow-md focus:shadow-lg"
          disabled={isLoading}
        />
        <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
          <button
            type="submit"
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200 disabled:opacity-50"
            disabled={isLoading || !query.trim()}
          >
            {isLoading ? (
              <div className="w-6 h-6 border-2 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            )}
          </button>
        </div>
      </div>
    </form>
  );
}
