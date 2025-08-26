import React, { useState, useEffect, useRef } from "react";

interface SearchInputProps {
  onSearch: (query: string) => Promise<void>;
  isLoading?: boolean;
  externalQuery?: string;
  shouldAutoSearch?: boolean;
}

/**
 * Search input component with smart state management
 * - Can be updated by external components (suggestions) one time
 * - User maintains full control for editing
 * - Auto-searches when suggestions are clicked
 * - Clears on click after search completion
 */
export default function SearchInput({
  onSearch,
  isLoading = false,
  externalQuery,
  shouldAutoSearch = false,
}: SearchInputProps) {
  const [query, setQuery] = useState("");
  const [hasExternalUpdate, setHasExternalUpdate] = useState(false);
  const [shouldClearOnClick, setShouldClearOnClick] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // Handle external query updates (from suggestions)
  useEffect(() => {
    if (externalQuery && !hasExternalUpdate) {
      setQuery(externalQuery);
      setHasExternalUpdate(true);

      // Auto-search if requested
      if (shouldAutoSearch) {
        onSearch(externalQuery);
      }
    }
  }, [externalQuery, hasExternalUpdate, shouldAutoSearch, onSearch]);

  // Reset external update flag when query changes manually
  useEffect(() => {
    if (hasExternalUpdate) {
      setHasExternalUpdate(false);
    }
  }, [query, hasExternalUpdate]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSearch(query.trim());
      setShouldClearOnClick(true);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as unknown as React.FormEvent);
    }
  };

  const handleInputClick = () => {
    // Clear the input if user clicks immediately after a search
    if (shouldClearOnClick) {
      setQuery("");
      setShouldClearOnClick(false);
      inputRef.current?.focus();
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
    // Reset clear flag when user starts typing
    if (shouldClearOnClick) {
      setShouldClearOnClick(false);
    }
  };

  return (
    <div className="flex-1 flex items-center justify-center px-4 lg:px-8 py-8 lg:py-16">
      <div className="w-full max-w-3xl mx-auto">
        {/* Search Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-6">
            Perplexity Clone
          </h1>
          <p className="text-xl lg:text-2xl text-gray-600 dark:text-gray-300">
            Ask anything. Get instant AI-powered answers.
          </p>
        </div>

        {/* Search Input */}
        <form onSubmit={handleSubmit} className="relative">
          <div className="relative">
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={handleInputChange}
              onClick={handleInputClick}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
              placeholder={
                shouldClearOnClick
                  ? "Click to clear and start new search..."
                  : "Ask me anything..."
              }
              className={`w-full px-8 py-6 text-xl lg:text-2xl bg-white dark:bg-gray-800 border-2 rounded-3xl shadow-2xl focus:outline-none transition-all duration-200 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 disabled:opacity-50 ${
                shouldClearOnClick
                  ? "border-blue-400 dark:border-blue-500 bg-blue-50 dark:bg-blue-900/20"
                  : "border-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-400"
              }`}
            />
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="absolute right-4 top-1/2 transform -translate-y-1/2 p-4 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-2xl transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <svg
                  className="w-6 h-6 animate-spin"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
              ) : (
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
