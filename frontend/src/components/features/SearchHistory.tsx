import React from "react";
import { toast } from "react-hot-toast";

interface SearchHistoryProps {
  onHistoryItemClick?: (query: string) => void;
}

/**
 * Search history component displaying recent searches
 * Supports both light and dark themes
 */
export default function SearchHistory({
  onHistoryItemClick,
}: SearchHistoryProps) {
  // Mock search history data - will be replaced with real data in future phases
  const items = [
    "What is artificial intelligence?",
    "How to learn React?",
    "Best programming languages 2024",
    "Climate change solutions",
    "Machine learning basics",
  ];

  const handleHistoryClick = (item: string) => {
    if (onHistoryItemClick) {
      onHistoryItemClick(item);
    } else {
      toast(
        "Search history functionality will be implemented in the next phase!",
        {
          duration: 3000,
          position: "top-center",
          style: {
            background: "#363636",
            color: "#fff",
          },
        },
      );
    }
  };

  return (
    <div className="space-y-3">
      {items.map((item, index) => (
        <button
          key={index}
          onClick={() => handleHistoryClick(item)}
          className="w-full text-left p-3 rounded-lg hover:bg-gray-50 hover:shadow-sm transition-all duration-200 text-gray-700 hover:text-gray-900 border border-transparent hover:border-gray-200 group dark:text-gray-300 dark:hover:text-gray-100 dark:hover:bg-gray-800 dark:hover:border-gray-700"
        >
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0 w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center group-hover:bg-blue-50 transition-colors duration-200 dark:bg-gray-700 dark:group-hover:bg-blue-900/20">
              <svg
                className="w-4 h-4 text-gray-500 group-hover:text-blue-500 transition-colors duration-200 dark:text-gray-400 dark:group-hover:text-blue-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate group-hover:text-blue-700 transition-colors duration-200 dark:text-white dark:group-hover:text-blue-300">
                {item}
              </p>
              <p className="text-xs text-gray-500 mt-0.5 dark:text-gray-400">
                Click to search again
              </p>
            </div>
            <div className="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
              <svg
                className="w-4 h-4 text-blue-500 dark:text-blue-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </div>
          </div>
        </button>
      ))}

      {items.length === 0 && (
        <div className="text-center py-8">
          <div className="w-12 h-12 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg
              className="w-6 h-6 text-gray-400 dark:text-gray-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            No search history yet
          </p>
          <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
            Your searches will appear here
          </p>
        </div>
      )}
    </div>
  );
}
