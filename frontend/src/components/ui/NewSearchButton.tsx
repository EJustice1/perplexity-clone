"use client";

import React from "react";
import { useRouter } from "next/navigation";

interface NewSearchButtonProps {
  onNewSearch?: () => void;
}

/**
 * New Search button component with enhanced styling
 * Supports both light and dark themes
 */
export default function NewSearchButton({ onNewSearch }: NewSearchButtonProps) {
  const router = useRouter();

  const handleNewSearch = () => {
    router.push("/");
    if (onNewSearch) {
      onNewSearch();
    }
  };

  return (
    <button
      onClick={handleNewSearch}
      className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 dark:from-blue-500 dark:to-blue-600 dark:hover:from-blue-600 dark:hover:to-blue-700 text-white font-semibold py-3 px-4 rounded-xl transition-all duration-200 flex items-center justify-center space-x-3 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:ring-offset-2 dark:focus:ring-offset-gray-900 focus:outline-none"
    >
      <div className="w-5 h-5 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
        <svg
          className="w-3 h-3 text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 4v16m8-8H4"
          />
        </svg>
      </div>
      <span>New Search</span>
    </button>
  );
}
