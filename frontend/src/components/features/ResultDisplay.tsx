import React from 'react';

interface WebSearchResult {
  title: string;
  url: string;
  snippet: string;
  source: string;
}

interface ExtractedContent {
  url: string;
  title: string;
  extracted_text: string;
  extraction_method: string;
  success: boolean;
  error_message?: string;
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
  extractedContent?: ExtractedContent[];
  contentSummary?: string;
  llmAnswer?: LLMAnswer;
  error?: string;
  hasSearched?: boolean;
  currentQuery?: string;
  onNewSearch?: () => void;
}

/**
 * Result display component for showing search results, loading states, and errors
 * Supports both light and dark themes
 */
export default function ResultDisplay({ 
  isLoading = false, 
  sources, 
  extractedContent,
  contentSummary,
  llmAnswer,
  error, 
  hasSearched = false, 
  currentQuery, 
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
          
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 lg:p-8">
            {/* Search Query Display */}
            {currentQuery && (
              <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                <h3 className="text-sm font-medium text-blue-800 dark:text-blue-200 mb-2">Search Query:</h3>
                <p className="text-lg text-blue-900 dark:text-blue-100 font-medium">&ldquo;{currentQuery}&rdquo;</p>
              </div>
            )}
            
            {/* LLM Answer Section */}
            {llmAnswer && llmAnswer.success && (
              <div className="mb-8 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl border border-blue-200 dark:border-blue-800">
                <div className="flex items-center mb-4">
                  <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mr-3">
                    <svg className="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h2 className="text-xl font-bold text-blue-900 dark:text-blue-100">AI-Generated Answer</h2>
                </div>
                <div className="prose prose-blue dark:prose-invert max-w-none">
                  <p className="text-blue-900 dark:text-blue-100 leading-relaxed text-lg">
                    {llmAnswer.answer}
                  </p>
                </div>
                {llmAnswer.tokens_used && (
                  <div className="mt-4 text-xs text-blue-600 dark:text-blue-400">
                    Generated using {llmAnswer.tokens_used} tokens
                  </div>
                )}
              </div>
            )}

            {/* Content Summary */}
            {contentSummary && (
              <div className="mb-6 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                <h3 className="text-sm font-medium text-green-800 dark:text-green-200 mb-2">Content Extraction Summary:</h3>
                <p className="text-green-900 dark:text-green-100">{contentSummary}</p>
              </div>
            )}
            
            {/* Extracted Content Section */}
            {extractedContent && extractedContent.length > 0 && (
              <div className="mb-8">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Extracted Content</h2>
                <div className="space-y-6">
                  {extractedContent.map((content, index) => (
                    <div key={index} className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-200">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                            <a 
                              href={content.url} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors duration-200"
                            >
                              {content.title || 'Untitled'}
                            </a>
                          </h3>
                          <p className="text-gray-600 dark:text-gray-400 text-sm mb-2">
                            {content.url}
                          </p>
                        </div>
                        <div className="ml-4">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            content.success 
                              ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-200' 
                              : 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-200'
                          }`}>
                            {content.success ? 'Success' : 'Failed'}
                          </span>
                        </div>
                      </div>
                      
                      {content.success ? (
                        <div>
                          <div className="mb-3">
                            <span className="text-xs font-medium text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                              Method: {content.extraction_method}
                            </span>
                          </div>
                          <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
                            <p className="text-gray-700 dark:text-gray-300 leading-relaxed text-sm">
                              {content.extracted_text}
                            </p>
                          </div>
                        </div>
                      ) : (
                        <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-4">
                          <p className="text-red-700 dark:text-red-300 text-sm">
                            <strong>Extraction failed:</strong> {content.error_message || 'Unknown error'}
                          </p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {/* Web Search Results Section */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Web Search Results</h2>
              <div className="space-y-6">
                {sources.map((source, index) => (
                  <div key={index} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-200">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      <a 
                        href={source.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors duration-200"
                      >
                        {source.title}
                      </a>
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-2">
                      {source.url}
                    </p>
                    <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                      {source.snippet}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
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
