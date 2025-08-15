import React from 'react';

interface SearchSuggestionsProps {
  onSearch: (query: string) => void;
  isLoading?: boolean;
}

/**
 * Search suggestions component with clickable search examples
 * Supports both light and dark themes
 */
export default function SearchSuggestions({ onSearch, isLoading = false }: SearchSuggestionsProps) {
  const suggestions = [
    "What is the capital of France?",
    "How does photosynthesis work?",
    "Explain quantum computing",
    "What are the benefits of exercise?",
    "How to learn programming?",
    "What is climate change?"
  ];

  const handleSuggestionClick = (suggestion: string) => {
    if (!isLoading) {
      onSearch(suggestion);
    }
  };

  return (
    <div className="px-4 lg:px-8 pb-8">
      <div className="max-w-3xl mx-auto">
        <h3 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-4 text-center">
          Try asking about:
        </h3>
        <div className="flex flex-wrap justify-center gap-3">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
              disabled={isLoading}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-full text-sm font-medium transition-colors duration-200 hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
