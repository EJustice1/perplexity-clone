import React from 'react';

interface SearchSuggestionsProps {
  onSearch: (query: string) => void;
  isLoading?: boolean;
}

/**
 * SearchSuggestions component displaying example search queries
 * Now interactive - clicking suggestions triggers searches
 */
export default function SearchSuggestions({ onSearch, isLoading = false }: SearchSuggestionsProps) {
  const suggestions = [
    "What is artificial intelligence?",
    "How to learn programming?",
    "Best books for beginners",
    "Latest tech trends"
  ];

  const handleSuggestionClick = (suggestion: string) => {
    if (!isLoading) {
      onSearch(suggestion);
    }
  };

  return (
    <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3">
      {suggestions.map((suggestion, index) => (
        <button
          key={index}
          onClick={() => handleSuggestionClick(suggestion)}
          className="p-3 text-left text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors duration-200 border border-gray-200 hover:border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={isLoading}
        >
          {suggestion}
        </button>
      ))}
    </div>
  );
}
