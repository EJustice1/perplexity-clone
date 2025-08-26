"use client";

import React, { useState, useEffect } from "react";
import ThemeToggle from "./ThemeToggle";

interface ThemeToggleWrapperProps {
  variant?: "sidebar" | "mobile";
}

/**
 * Wrapper component that conditionally renders ThemeToggle
 * Prevents SSR issues by only rendering on the client side
 */
export default function ThemeToggleWrapper({
  variant = "sidebar",
}: ThemeToggleWrapperProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    // Return a placeholder with the same dimensions to prevent layout shift
    return (
      <div
        className={`flex items-center space-x-3 px-3 py-2.5 rounded-lg w-full ${
          variant === "sidebar"
            ? "text-gray-700 dark:text-gray-300"
            : "text-gray-700"
        }`}
      >
        <span className="flex-shrink-0 text-gray-500 dark:text-gray-400">
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
            />
          </svg>
        </span>
        <span className="font-medium text-sm">Loading...</span>
      </div>
    );
  }

  return <ThemeToggle variant={variant} />;
}
