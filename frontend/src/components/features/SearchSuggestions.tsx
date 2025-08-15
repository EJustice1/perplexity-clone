import React from 'react';

interface SearchSuggestionsProps {
  disabled?: boolean;
}

/**
 * SearchSuggestions component displaying example search queries
 * Currently disabled as per Part 1 Stage 1 requirements
 */
export default function SearchSuggestions({ disabled = true }: SearchSuggestionsProps) {
  const suggestions = [
    "What is artificial intelligence?",
    "How to learn programming?",
    "Best books for beginners",
    "Latest tech trends"
  ];

  return (
    <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3">
      {suggestions.map((suggestion, index) => (
        <button
          key={index}
          className="p-3 text-left text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors duration-200 border border-gray-200 hover:border-gray-300"
          disabled={disabled}
        >
          {suggestion}
        </button>
      ))}
    </div>
  );
}
