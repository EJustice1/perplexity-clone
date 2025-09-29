import React from "react";

/**
 * Subscribed topics placeholder component
 * Displays informational messaging until subscription management is implemented
 * Supports both light and dark themes
 */
export default function SubscribedTopics() {
  return (
    <div className="max-w-3xl mx-auto p-8">
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-dashed border-blue-400 dark:border-blue-500/60 p-8 text-center shadow-sm">
        <div className="mb-4 flex justify-center">
          <span className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-blue-100 text-blue-600 dark:bg-blue-500/20 dark:text-blue-300">
            <svg
              className="w-7 h-7"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 11H5m14 0a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2m14 0V7a2 2 0 00-2-2h-3.34a2 2 0 01-1.414-.586l-.828-.828A2 2 0 0011.172 3H8a2 2 0 00-2 2v2m13 4H5"
              />
            </svg>
          </span>
        </div>
        <h1 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
          Subscribed Topics
        </h1>
        <p className="text-gray-600 dark:text-gray-300 mb-4">
          Stay tuned! Soon you&rsquo;ll be able to follow topics and get tailored updates right here.
        </p>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          This feature is scheduled for a future phase. For now, feel free to explore the latest answers and insights.
        </p>
      </div>
    </div>
  );
}

