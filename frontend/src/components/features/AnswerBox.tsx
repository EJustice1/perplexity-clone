import React, { useState } from "react";
import { MarkdownRenderer, TabNavigation, SourcesList } from "../ui";

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

interface AnswerBoxProps {
  question: string;
  answer?: LLMAnswer;
  sources?: WebSearchResult[];
  revisedQuery?: string;
  className?: string;
}

/**
 * Main answer box component with tabs for Answer and Sources
 * Displays question, answer content, and sources in a clean layout
 */
export const AnswerBox: React.FC<AnswerBoxProps> = ({
  question,
  answer,
  sources,
  revisedQuery,
  className = "",
}) => {
  const [activeTab, setActiveTab] = useState<"answer" | "sources">("answer");

  const tabs = [
    {
      id: "answer",
      label: "Answer",
      icon: (
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
          />
        </svg>
      ),
    },
    {
      id: "sources",
      label: "Sources",
      icon: (
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
          />
        </svg>
      ),
    },
  ];

  return (
    <div
      className={`bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden ${className}`}
    >
      {/* Question Header */}
      <div className="px-6 py-4 bg-blue-50 dark:bg-blue-900/20 border-b border-blue-200 dark:border-blue-800">
        <h2 className="text-lg font-semibold text-blue-900 dark:text-blue-100">
          Question Asked:
        </h2>
        <p className="text-blue-800 dark:text-blue-200 mt-1">
          &ldquo;{question}&rdquo;
        </p>
      </div>

      {/* Tab Navigation */}
      <TabNavigation
        tabs={tabs}
        activeTab={activeTab}
        onTabChange={(tabId) => setActiveTab(tabId as "answer" | "sources")}
      />

      {/* Tab Content */}
      <div className="p-6">
        {activeTab === "answer" ? (
          <div role="tabpanel" id="answer-panel" aria-labelledby="answer-tab">
            {answer && answer.success ? (
              <div>
                {/* Revised Query Display */}
                {revisedQuery && revisedQuery !== question && (
                  <div className="mb-6 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                    <div className="flex items-start space-x-2">
                      <svg
                        className="w-5 h-5 text-green-600 dark:text-green-400 mt-0.5 flex-shrink-0"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                      <div>
                        <p className="text-sm font-medium text-green-800 dark:text-green-200 mb-1">
                          Revised Query:
                        </p>
                        <p className="text-sm text-green-700 dark:text-green-300">
                          &ldquo;{revisedQuery}&rdquo;
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Sources Quick Links */}
                {sources && sources.length > 0 && (
                  <div className="mb-6">
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Sources:
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {sources.map((source, index) => (
                        <a
                          key={index}
                          href={source.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center px-3 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 text-sm font-medium rounded-full hover:bg-blue-200 dark:hover:bg-blue-900/30 transition-colors duration-200"
                        >
                          [{index + 1}]
                        </a>
                      ))}
                    </div>
                  </div>
                )}

                {/* Main Answer Content */}
                <MarkdownRenderer content={answer.answer} />

                {/* Token Usage */}
                {answer.tokens_used && (
                  <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
                      Generated using {answer.tokens_used} tokens
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-8">
                <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg
                    className="w-8 h-8 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.29-1.009-5.824-2.563M15 9.34c-.665-1.07-1.524-1.994-2.56-2.729A7.965 7.965 0 0012 6.5c-1.384 0-2.662.476-3.67 1.275M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
                <p className="text-gray-500 dark:text-gray-400">
                  {answer?.error_message || "No answer available"}
                </p>
              </div>
            )}
          </div>
        ) : (
          <div role="tabpanel" id="sources-panel" aria-labelledby="sources-tab">
            <SourcesList sources={sources || []} />
          </div>
        )}
      </div>
    </div>
  );
};

export default AnswerBox;
