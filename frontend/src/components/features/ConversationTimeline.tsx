import React, { useState } from 'react';
import { MarkdownRenderer } from '../ui';

// Separate component for conversation entry to allow useState
function ConversationEntry({ entry }: { entry: ConversationEntry }) {
  const [activeTab, setActiveTab] = useState<'answer' | 'sources'>('answer');
  
  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 lg:p-8">
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

      {/* Response Card with Tabs */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
        {/* Tabs */}
        <div className="flex border-b border-gray-200 dark:border-gray-700">
          <button
            onClick={() => setActiveTab('answer')}
            className={`flex-1 px-6 py-4 text-sm font-medium transition-colors duration-200 ${
              activeTab === 'answer'
                ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400 bg-blue-50 dark:bg-blue-900/20'
                : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50'
            }`}
          >
            <div className="flex items-center justify-center space-x-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <span>Answer</span>
            </div>
          </button>
          <button
            onClick={() => setActiveTab('sources')}
            className={`flex-1 px-6 py-4 text-sm font-medium transition-colors duration-200 ${
              activeTab === 'sources'
                ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400 bg-blue-50 dark:bg-blue-900/20'
                : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50'
            }`}
          >
            <div className="flex items-center justify-center space-x-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              <span>Sources</span>
            </div>
          </button>
        </div>

        {/* Tab Content */}
        <div className="p-6 lg:p-8">
          {activeTab === 'answer' ? (
            /* Answer Tab Content */
            <div>
              {entry.llmAnswer && entry.llmAnswer.success ? (
                <div>
                  <MarkdownRenderer content={entry.llmAnswer.answer} />
                  {entry.llmAnswer.tokens_used && (
                    <div className="mt-4 text-xs text-gray-500 dark:text-gray-400">
                      Generated using {entry.llmAnswer.tokens_used} tokens
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-gray-500 dark:text-gray-400 text-center py-8">
                  <p>No AI answer available</p>
                </div>
              )}
            </div>
          ) : (
            /* Sources Tab Content */
            <div>
              {/* Query Enhancement Information */}
              {entry.originalQuery && entry.enhancedQuery && (
                <div className="mb-6 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                  <h3 className="text-sm font-medium text-green-800 dark:text-green-200 mb-2">Query Enhancement:</h3>
                  <div className="space-y-2">
                    <div>
                      <span className="text-xs text-green-700 dark:text-green-300 font-medium">Original:</span>
                      <p className="text-sm text-green-900 dark:text-green-100">&ldquo;{entry.originalQuery}&rdquo;</p>
                    </div>
                    <div>
                      <span className="text-xs text-green-700 dark:text-green-300 font-medium">Enhanced:</span>
                      <p className="text-sm text-green-900 dark:text-green-100 font-medium">&ldquo;{entry.enhancedQuery}&rdquo;</p>
                    </div>
                    {entry.queryEnhancementSuccess !== undefined && (
                      <div className="text-xs text-green-700 dark:text-green-300">
                        Status: {entry.queryEnhancementSuccess ? '✅ Enhanced' : '⚠️ Fallback to original'}
                      </div>
                    )}
                  </div>
                </div>
              )}
              
              <div className="space-y-3">
                {entry.sources.map((source, sourceIndex) => (
                  <div key={sourceIndex} className="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-200 dark:border-gray-600">
                    <div className="flex-shrink-0 w-6 h-6 bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center text-xs font-medium text-blue-600 dark:text-blue-400">
                      {sourceIndex + 1}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h5 className="text-sm font-medium text-gray-900 dark:text-white mb-1">
                        <a 
                          href={source.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors duration-200"
                        >
                          {source.title}
                        </a>
                      </h5>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mb-1 truncate">
                        {source.url}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-300 line-clamp-2">
                        {source.snippet}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

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

interface ConversationEntry {
  query: string;
  sources: WebSearchResult[];
  extractedContent: ExtractedContent[];
  contentSummary?: string;
  llmAnswer?: LLMAnswer;
  originalQuery?: string;
  enhancedQuery?: string;
  queryEnhancementSuccess?: boolean;
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
            <ConversationEntry key={index} entry={entry} />
          ))}
        </div>
      </div>
    </div>
  );
}
