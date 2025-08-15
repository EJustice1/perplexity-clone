import React from 'react';

interface ResultDisplayProps {
  isLoading?: boolean;
  result?: string;
  error?: string;
  hasSearched?: boolean;
}

/**
 * ResultDisplay component showing search results or appropriate states
 * Handles loading, success, error, and initial states
 */
export default function ResultDisplay({ isLoading = false, result, error, hasSearched = false }: ResultDisplayProps) {
  if (isLoading) {
    return (
      <div className="px-8 pb-8">
        <div className="max-w-3xl mx-auto">
          <div className="bg-white rounded-2xl border border-gray-200 p-8 text-center">
            <div className="w-16 h-16 border-4 border-gray-200 border-t-blue-500 rounded-full animate-spin mx-auto mb-4"></div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Searching...
            </h3>
            <p className="text-gray-600">
              Finding the best answers for you
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="px-8 pb-8">
        <div className="max-w-3xl mx-auto">
          <div className="bg-red-50 rounded-2xl border border-red-200 p-8 text-center">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-red-900 mb-2">
              Something went wrong
            </h3>
            <p className="text-red-700 mb-4">
              {error}
            </p>
            <p className="text-sm text-red-600">
              Please try again or check your connection
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (result && hasSearched) {
    return (
      <div className="px-8 pb-8">
        <div className="max-w-3xl mx-auto">
          <div className="bg-white rounded-2xl border border-gray-200 p-8">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Result
            </h3>
            <div className="bg-gray-50 p-6 rounded-xl">
              <p className="text-lg text-gray-700 font-mono break-words leading-relaxed">
                {result}
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Initial state
  return (
    <div className="px-8 pb-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-2xl border border-gray-200 p-8 text-center">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Ready to search
          </h3>
          <p className="text-gray-600">
            Type your question above to get started
          </p>
        </div>
      </div>
    </div>
  );
}
