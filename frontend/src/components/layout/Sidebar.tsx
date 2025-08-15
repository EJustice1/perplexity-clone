import React from 'react';
import { AppLogo, UserProfile, NewSearchButton, Navigation, ThemeToggleWrapper } from '../ui';
import { SearchHistory } from '../features';

interface SidebarProps {
  onNewSearch?: () => void;
  onHistoryItemClick?: (query: string) => void;
}

/**
 * Sidebar component with improved industry standard styling
 * Includes user profile, navigation, search history, theme toggle, and new search button
 */
export default function Sidebar({ onNewSearch, onHistoryItemClick }: SidebarProps) {
  return (
    <div className="w-80 h-full bg-white border-r border-gray-200 flex flex-col overflow-hidden shadow-sm dark:bg-gray-900 dark:border-gray-700">
      {/* App Title */}
      <div className="flex-shrink-0 p-6 border-b border-gray-100 bg-gradient-to-br from-gray-50 to-white dark:from-gray-800 dark:to-gray-900 dark:border-gray-700">
        <AppLogo />
      </div>

      {/* User Profile */}
      <div className="flex-shrink-0 p-6 border-b border-gray-100 bg-white dark:bg-gray-900 dark:border-gray-700">
        <UserProfile variant="sidebar" />
      </div>

      {/* Navigation */}
      <div className="flex-shrink-0 px-6 py-5 border-b border-gray-100 bg-gray-50 dark:bg-gray-800 dark:border-gray-700">
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 dark:text-gray-400">
          Navigation
        </h3>
        <Navigation variant="sidebar" />
      </div>

      {/* Search History */}
      <div className="flex-1 px-6 py-5 overflow-y-auto bg-white dark:bg-gray-900">
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 dark:text-gray-400">
          Recent Searches
        </h3>
        <SearchHistory variant="sidebar" onHistoryItemClick={onHistoryItemClick} />
      </div>

      {/* Theme Toggle */}
      <div className="flex-shrink-0 px-6 py-4 border-t border-gray-100 bg-gray-50 dark:bg-gray-800 dark:border-gray-700">
        <ThemeToggleWrapper variant="sidebar" />
      </div>

      {/* New Search Button */}
      <div className="flex-shrink-0 p-6 border-t border-gray-100 bg-gradient-to-t from-gray-50 to-white dark:from-gray-800 dark:to-gray-900 dark:border-gray-700">
        <NewSearchButton onNewSearch={onNewSearch} />
      </div>
    </div>
  );
}

