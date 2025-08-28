import React, { useState, useEffect, useRef } from "react";
import { MarkdownRenderer, LoadingAnimation } from "../ui";

// Separate component for conversation entry to allow useState
function ConversationEntry({ entry }: { entry: ConversationEntry }) {
  const [activeTab, setActiveTab] = useState<"answer" | "sources">("answer");

  return (
    <div className="mb-16 last:mb-0" data-conversation-entry>
      {/* Question - Big Text */}
      <div className="mb-10">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white leading-tight">
          {entry.query}
        </h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
          {entry.timestamp.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </p>
      </div>

      {/* Tabs - Clean without borders */}
      <div className="flex mb-8">
        <button
          onClick={() => setActiveTab("answer")}
          className={`px-6 py-3 text-sm font-medium transition-colors duration-200 ${
            activeTab === "answer"
              ? "text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400 bg-blue-50 dark:bg-blue-900/20"
              : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
          }`}
        >
          Answer
        </button>
        <button
          onClick={() => setActiveTab("sources")}
          className={`px-6 py-3 text-sm font-medium transition-colors duration-200 ${
            activeTab === "sources"
              ? "text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400 bg-blue-50 dark:bg-blue-900/20"
              : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
          }`}
        >
          Sources
        </button>
      </div>

      {/* Tab Content */}
      <div className="mb-8">
        {activeTab === "answer" ? (
          /* Answer Tab Content */
          <div>
            {entry.llmAnswer && entry.llmAnswer.success ? (
              <div className="prose prose-gray dark:prose-invert max-w-none">
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
                <h3 className="text-sm font-medium text-green-800 dark:text-green-200 mb-2">
                  Query Enhancement:
                </h3>
                <div className="space-y-2">
                  <div>
                    <span className="text-xs text-green-700 dark:text-green-300 font-medium">
                      Original:
                    </span>
                    <p className="text-sm text-green-900 dark:text-green-100">
                      &ldquo;{entry.originalQuery}&rdquo;
                    </p>
                  </div>
                  <div>
                    <span className="text-xs text-green-700 dark:text-green-300 font-medium">
                      Enhanced:
                    </span>
                    <p className="text-sm text-green-900 dark:text-green-100 font-medium">
                      &ldquo;{entry.enhancedQuery}&rdquo;
                    </p>
                  </div>
                  {entry.queryEnhancementSuccess !== undefined && (
                    <div className="text-xs text-green-700 dark:text-green-300">
                      Status:{" "}
                      {entry.queryEnhancementSuccess
                        ? "✅ Enhanced"
                        : "⚠️ Fallback to original"}
                    </div>
                  )}
                </div>
              </div>
            )}

            <div className="space-y-4">
              {entry.sources.map((source, sourceIndex) => (
                <div
                  key={sourceIndex}
                  className="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg"
                >
                  <h5 className="text-sm font-medium text-gray-900 dark:text-white mb-2">
                    <a
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors duration-200"
                    >
                      {source.title}
                    </a>
                  </h5>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">
                    {source.url}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    {source.snippet}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Loading entry component for current question
const LoadingEntry = React.forwardRef<HTMLDivElement, { query: string }>(
  ({ query }, ref) => {
      return (
    <div ref={ref} data-current-question="true" className="mb-16">
              {/* Question - Big Text */}
      <div className="mb-10">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white leading-tight">
          {query}
        </h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
          {new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </p>
      </div>

        {/* Loading Animation */}
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <LoadingAnimation size="lg" className="mb-4" />
            <p className="text-gray-600 dark:text-gray-400">
              Searching for answers...
            </p>
          </div>
        </div>
      </div>
    );
  }
);

LoadingEntry.displayName = 'LoadingEntry';

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
  currentQuery?: string;
}

/**
 * Conversation timeline component that displays search history as a continuous chain
 * Shows original question at top, most recent at bottom with loading animation for current question
 * Supports both light and dark themes
 */
export default function ConversationTimeline({
  conversationHistory,
  onNewSearch,
  error,
  isLoading,
  currentQuery,
}: ConversationTimelineProps) {
  const currentQuestionRef = useRef<HTMLDivElement>(null);
  const stickyHeaderRef = useRef<HTMLDivElement>(null);

  // Simple scroll to top when loading starts (question appears)
  useEffect(() => {
    if (isLoading && currentQuery) {
      // Use setTimeout to ensure DOM is fully rendered before scrolling
      setTimeout(() => {
        if (currentQuestionRef.current) {
          console.log('Attempting to scroll, element found:', currentQuestionRef.current);
          
          try {
            // Find the actual scrollable container (main element with overflow-auto)
            const scrollableContainer = currentQuestionRef.current?.closest('main[class*="overflow-auto"]') || 
                                     currentQuestionRef.current?.closest('main') ||
                                     document.documentElement;
            
            // Get the element's position relative to the scrollable container
            const elementRect = currentQuestionRef.current.getBoundingClientRect();
            const containerRect = scrollableContainer.getBoundingClientRect();
            
            // Calculate scroll position relative to the container
            const elementTop = elementRect.top + window.pageYOffset;
            const containerTop = containerRect.top + window.pageYOffset;
            const relativePosition = elementTop - containerTop;
            
            // Get sticky header height
            const headerHeight = stickyHeaderRef.current?.offsetHeight || 72;
            const padding = 20; // Additional padding below header
            
            // Calculate final scroll position
            const scrollPosition = relativePosition - headerHeight - padding;
            
            console.log('Scrolling to position below sticky header:', {
              elementTop,
              containerTop,
              relativePosition,
              headerHeight,
              padding,
              scrollPosition,
              scrollableContainer: scrollableContainer.tagName
            });
            
            // Scroll the correct container
            if (scrollableContainer === document.documentElement) {
              // If it's the document, use scrollTop
              document.documentElement.scrollTop = scrollPosition;
            } else {
              // If it's a main element, scroll that container
              scrollableContainer.scrollTop = scrollPosition;
            }
            
          } catch (error) {
            console.error('Scroll error:', error);
          }
        } else {
          console.log('Element ref not found');
        }
      }, 100); // Small delay to ensure DOM is ready
    }
  }, [isLoading, currentQuery]);

  if (conversationHistory.length === 0 && !isLoading) {
    return null;
  }

  // Show error if there is one
  if (error) {
    return (
      <div className="flex-1 px-4 lg:px-8 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center max-w-2xl">
            <div className="w-16 h-16 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg
                className="w-8 h-8 text-red-600 dark:text-red-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Something went wrong
            </h3>
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
    <div 
      data-conversation-container
      className="flex-1 relative"
    >
      {/* Sticky New Search Button - Full Width Background */}
      <div ref={stickyHeaderRef} className="sticky top-0 z-10 w-full bg-white dark:bg-gray-900 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 lg:px-8 py-4">
          <div className="text-right">
            <button
              onClick={onNewSearch}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg transition-colors duration-200 font-medium"
            >
              ← New Search
            </button>
          </div>
        </div>
      </div>

      {/* Conversation Timeline - Continuous Chain */}
      <div className="px-4 lg:px-8 pt-4 pb-8">
        <div className="max-w-4xl mx-auto">
          <div className="space-y-0">
            {/* Show conversation history */}
            {conversationHistory.map((entry, index) => (
              <ConversationEntry key={index} entry={entry} />
            ))}
            
            {/* Show loading animation for current question if searching */}
            {isLoading && currentQuery && (
              <LoadingEntry 
                ref={currentQuestionRef} 
                query={currentQuery}
              />
            )}
            
            {/* Filler content to ensure scrollable space */}
            {isLoading && currentQuery && (
              <div className="h-screen bg-transparent"></div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
