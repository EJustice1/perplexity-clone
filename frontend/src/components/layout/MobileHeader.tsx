import React, { useState } from "react";
import {
  AppLogo,
  UserProfile,
  NewSearchButton,
  Navigation,
  ThemeToggleWrapper,
} from "../ui";

/**
 * Mobile header component with hamburger menu
 * Includes all sidebar functionality in mobile-friendly format
 */
export default function MobileHeader() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <div className="lg:hidden bg-white border-b border-gray-200 px-4 py-3 relative z-40 dark:bg-gray-900 dark:border-gray-700">
      <div className="flex items-center justify-between">
        {/* App Logo */}
        <div className="flex items-center space-x-3">
          <AppLogo />
        </div>

        {/* Hamburger Menu Button */}
        <button
          onClick={toggleMenu}
          className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 dark:text-gray-300 dark:hover:text-gray-100 dark:hover:bg-gray-800"
          aria-label="Toggle menu"
          aria-expanded={isMenuOpen}
        >
          <svg
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="absolute top-full left-0 right-0 bg-white border-b border-gray-200 shadow-lg z-50 dark:bg-gray-900 dark:border-gray-700">
          <div className="p-4 space-y-4 max-h-[80vh] overflow-y-auto">
            {/* App Title */}
            <div className="pb-4 border-b border-gray-200 dark:border-gray-700">
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                Perplexity Clone
              </h1>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                AI-Powered Search Engine
              </p>
            </div>

            {/* User Profile */}
            <div className="pb-4 border-b border-gray-200 dark:border-gray-700">
              <UserProfile variant="mobile" />
            </div>

            {/* Navigation */}
            <div className="pb-4 border-b border-gray-200 dark:border-gray-700">
              <Navigation variant="mobile" />
            </div>

            {/* Theme Toggle */}
            <div className="pb-4 border-b border-gray-200 dark:border-gray-700">
              <ThemeToggleWrapper variant="mobile" />
            </div>

            {/* New Search Button */}
            <div>
              <NewSearchButton />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
