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
  citations?: string[];
  subQueries: string[];
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
 * 2. Regular entry - renders the question, answer, and sources with timeline-specific styling
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
        <div ref={ref} className={`mb-16 last:mb-0 ${isLast ? "min-h-screen" : ""}`} data-timeline-entry>
          {/* Question */}
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

          {/* Tabs */}
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
                  ? "text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400 bg-blue-50 dark:bg-blue-400/30"
                  : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
              }`}
            >
              Sources
            </button>
          </div>

          {/* Tab Content */}
          <div className={`mb-8 ${isLast ? "flex-1 min-h-[calc(100vh-400px)]" : ""}`}>
            {activeTab === "answer" ? (
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
              <div className={isLast ? "h-full" : ""}>
                {entry.subQueries.length > 0 && (
                  <div className="mb-6">
                    <h3 className="text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
                      Sub-queries
                    </h3>
                    <ul className="space-y-2">
                      {entry.subQueries.map((query, idx) => (
                        <li
                          key={`${query}-${idx}`}
                          className="text-xs text-gray-600 dark:text-gray-300 border-l-2 border-blue-500 pl-3"
                        >
                          {query}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {entry.citations && entry.citations.length > 0 && (
                  <div className="mb-6">
                    <h3 className="text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
                      Citations
                    </h3>
                    <ul className="space-y-2">
                      {entry.citations.map((url, idx) => (
                        <li
                          key={`${url}-${idx}`}
                          className="text-xs text-blue-600 dark:text-blue-400 break-words"
                        >
                          <a
                            href={url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="hover:underline"
                          >
                            {url}
                          </a>
                        </li>
                      ))}
                    </ul>
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
