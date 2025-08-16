import React from 'react';

interface WebSearchResult {
  title: string;
  url: string;
  snippet: string;
  source: string;
}

interface ConversationEntry {
  query: string;
  sources: WebSearchResult[];
  timestamp: Date;
}

interface ConversationTimelineProps {
  conversationHistory: ConversationEntry[];
  onNewSearch: () => void;
  error?: string;
  isLoading?: boolean;
}

/**
 * Conversation timeline component that displays search history
 * Shows original question at top, most recent at bottom
 * Supports both light and dark themes
 */
export default function ConversationTimeline({ conversationHistory, onNewSearch, error, isLoading }: ConversationTimelineProps) {
  if (conversationHistory.length === 0) {
    return null;
  }

  // Show loading state
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

  // Show error if there is one
  if (error) {
    return (
      <div className="flex-1 px-4 lg:px-8 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center max-w-2xl">
            <div className="w-16 h-16 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Something went wrong</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">{error}</p>
            <button 
              onClick={onNewSearch} 
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors duration-200"
            >
              Try again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 px-4 lg:px-8 py-8 overflow-y-auto">
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

        {/* Conversation Timeline */}
        <div className="space-y-8">
          {conversationHistory.map((entry, index) => (
            <div key={index} className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 lg:p-8">
              {/* Question */}
              <div className="mb-6">
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <svg className="w-4 h-4 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      {entry.query}
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {entry.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </div>
              </div>

              {/* Search Results */}
              <div className="space-y-4">
                <h4 className="text-md font-medium text-gray-700 dark:text-gray-300">
                  Web Search Results:
                </h4>
                <div className="space-y-4">
                  {entry.sources.map((source, sourceIndex) => (
                    <div key={sourceIndex} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-200">
                      <h5 className="text-md font-semibold text-gray-900 dark:text-white mb-2">
                        <a 
                          href={source.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors duration-200"
                        >
                          {source.title}
                        </a>
                      </h5>
                      <p className="text-gray-600 dark:text-gray-400 text-sm mb-2">
                        {source.url}
                      </p>
                      <p className="text-gray-700 dark:text-gray-300 leading-relaxed text-sm">
                        {source.snippet}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
