import React from 'react';
import { AnswerBox } from '.';

interface WebSearchResult {
  title: string;
  url: string;
  snippet: string;
  source: string;
}

interface LLMAnswer {
  answer: string;
  success: boolean;
  error_message?: string;
  tokens_used?: number;
}

interface ResultDisplayProps {
  isLoading?: boolean;
  sources?: WebSearchResult[];
  llmAnswer?: LLMAnswer;
  error?: string;
  hasSearched?: boolean;
  currentQuery?: string;
  originalQuery?: string;
  enhancedQuery?: string;
  onNewSearch?: () => void;
}

/**
 * Result display component for showing search results, loading states, and errors
 * Supports both light and dark themes
 */
export default function ResultDisplay({ 
  isLoading = false, 
  sources, 
  llmAnswer,
  error, 
  hasSearched = false, 
  currentQuery, 
  originalQuery,
  enhancedQuery,
  onNewSearch 
}: ResultDisplayProps) {
  if (isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center px-4 lg:px-8">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-200 dark:border-blue-800 border-t-blue-600 dark:border-t-blue-400 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-lg text-gray-600 dark:text-gray-400">Searching for answers...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 flex items-center justify-center px-4 lg:px-8">
        <div className="text-center max-w-2xl">
          <div className="w-16 h-16 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Something went wrong</h3>
          <p className="text-gray-600 dark:text-gray-400 mb-4">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors duration-200"
          >
            Try again
          </button>
        </div>
      </div>
    );
  }

  if (sources && hasSearched) {
    return (
      <div className="flex-1 px-4 lg:px-8 py-8">
        <div className="max-w-4xl mx-auto">
          {/* New Search Button */}
          <div className="mb-6 text-right">
            <button 
              onClick={onNewSearch} 
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg transition-colors duration-200 font-medium"
            >
              ← New Search
            </button>
          </div>
          
          {/* New Answer Box Component */}
          <AnswerBox
            question={currentQuery || originalQuery || ''}
            answer={llmAnswer}
            sources={sources}
            revisedQuery={enhancedQuery && enhancedQuery !== (currentQuery || originalQuery) ? enhancedQuery : undefined}
          />
        </div>
      </div>
    );
  }

  // Initial state - no search performed yet
  return (
    <div className="flex-1 flex items-center justify-center px-4 lg:px-8">
      <div className="text-center max-w-2xl">
        <div className="w-24 h-24 bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-12 h-12 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Ready to search?</h3>
        <p className="text-lg text-gray-600 dark:text-gray-400">
          Type your question above and get instant AI-powered answers to anything you want to know.
        </p>
      </div>
    </div>
  );
}
