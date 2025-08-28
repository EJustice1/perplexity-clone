import React, { useState } from "react";
import { MarkdownRenderer, LoadingAnimation } from "../ui";

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

interface TimelineEntryProps {
  entry?: ConversationEntry;
  isLast: boolean;
  isLoading: boolean;
  currentQuery?: string;
}

/**
 * Standalone timeline entry component that contains query, answer, and loading states
 * 
 * This component handles three different states:
 * 1. Loading state - shows question with loading animation
 * 2. Regular entry - shows completed question with answer and sources
 * 3. Empty state - returns null (should not occur in normal usage)
 * 
 * @param entry - The conversation entry data (undefined for loading state)
 * @param isLast - Whether this entry should have minimum height (true for current question)
 * @param isLoading - Whether we're currently in a loading state
 * @param currentQuery - The current query being processed (for loading state)
 * @returns JSX element for the timeline entry
 */
const TimelineEntry = React.forwardRef<HTMLDivElement, TimelineEntryProps>(
  ({ entry, isLast, isLoading, currentQuery }, ref) => {
    const [activeTab, setActiveTab] = useState<"answer" | "sources">("answer");

    // If this is the current loading entry, show the loading state
    if (isLoading && currentQuery && !entry) {
      return (
        <div ref={ref} className={`mb-16 last:mb-0 ${isLast ? "min-h-screen" : ""}`} data-timeline-entry>
          {/* Question - Big Text */}
          <div className="mb-10">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white leading-tight">
              {currentQuery}
            </h2>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
              {new Date().toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </p>
          </div>

          {/* Loading Animation - Fills all available area */}
          <div className="flex-1 flex items-center justify-center py-12 min-h-[calc(100vh-300px)]">
            <div className="text-center">
              <LoadingAnimation size="lg" className="mb-4" />
              <p className="text-gray-500 dark:text-gray-400">
                Searching for answers...
              </p>
            </div>
          </div>
        </div>
      );
    }

    // If this is a regular entry, show the conversation
    if (entry) {
      return (
        <div className={`mb-16 last:mb-0 ${isLast ? "min-h-screen" : ""}`} data-timeline-entry>
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
                  ? "text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400 bg-blue-50 dark:bg-blue-400"
                  : "text-gray-500 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
              }`}
            >
              Sources
            </button>
          </div>

          {/* Tab Content - Fills available area when isLast is true */}
          <div className={`mb-8 ${isLast ? "flex-1 min-h-[calc(100vh-400px)]" : ""}`}>
            {activeTab === "answer" ? (
              /* Answer Tab Content */
              <div className={isLast ? "h-full" : ""}>
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
              <div className={isLast ? "h-full" : ""}>
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

    return null;
  }
);

TimelineEntry.displayName = 'TimelineEntry';

export default TimelineEntry;
export type { TimelineEntryProps, ConversationEntry, WebSearchResult, ExtractedContent, LLMAnswer };
