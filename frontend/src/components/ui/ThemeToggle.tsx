"use client";

import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';

interface ThemeToggleProps {
  variant?: 'sidebar' | 'mobile';
}

/**
 * Theme toggle button component
 * Switches between light and dark modes
 * Uses sun/moon icons to represent current theme
 * Client-only component to prevent SSR issues
 */
export default function ThemeToggle({ variant = 'sidebar' }: ThemeToggleProps) {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className={`flex items-center space-x-3 px-3 py-2.5 rounded-lg text-left transition-all duration-200 w-full ${
        variant === 'sidebar' 
          ? 'text-gray-700 hover:bg-gray-100 hover:text-gray-900 hover:shadow-sm dark:text-gray-300 dark:hover:bg-gray-800 dark:hover:text-gray-100' 
          : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
      }`}
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
    >
      <span className="flex-shrink-0 text-gray-500 dark:text-gray-400">
        {theme === 'light' ? (
          // Moon icon for dark mode
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
        ) : (
          // Sun icon for light mode
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        )}
      </span>
      <span className={`font-medium ${variant === 'mobile' ? 'text-sm' : 'text-sm'}`}>
        {theme === 'light' ? 'Dark Mode' : 'Light Mode'}
      </span>
    </button>
  );
}
