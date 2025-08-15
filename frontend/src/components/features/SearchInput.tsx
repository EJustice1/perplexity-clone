import React from 'react';

interface SearchInputProps {
  disabled?: boolean;
}

/**
 * SearchInput component for the main search interface
 * Currently disabled as per Part 1 Stage 1 requirements
 */
export default function SearchInput({ disabled = true }: SearchInputProps) {
  return (
    <div className="relative">
      <div className="relative">
        <input
          type="text"
          placeholder="Ask me anything..."
          className="w-full px-6 py-4 text-lg border border-gray-300 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all shadow-sm hover:shadow-md focus:shadow-lg"
          disabled={disabled}
        />
        <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
          <button
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
            disabled={disabled}
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
