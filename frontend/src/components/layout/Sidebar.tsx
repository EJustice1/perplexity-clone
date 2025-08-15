import React from 'react';
import { UserProfile, AppLogo, NewSearchButton, Navigation } from '../ui';
import { SearchHistory } from '../features';

interface SidebarProps {
  onNewSearch?: () => void;
  onHistoryItemClick?: (query: string) => void;
}

/**
 * Sidebar component following industry standard web layouts
 * Uses proper spacing, typography, and visual hierarchy
 */
export default function Sidebar({ onNewSearch, onHistoryItemClick }: SidebarProps) {
  return (
    <div className="w-80 h-full bg-white border-r border-gray-200 flex flex-col overflow-hidden shadow-sm">
      {/* App Title - At top, fixed height with proper branding */}
      <div className="flex-shrink-0 p-6 border-b border-gray-100 bg-gradient-to-br from-gray-50 to-white">
        <AppLogo variant="sidebar" showSubtitle={true} />
      </div>

      {/* User Profile Section - Fixed height with improved styling */}
      <div className="flex-shrink-0 p-6 border-b border-gray-100 bg-white">
        <UserProfile variant="sidebar" />
      </div>

      {/* Navigation Section - Fixed height with better visual separation */}
      <div className="flex-shrink-0 px-6 py-5 border-b border-gray-100 bg-gray-50">
        <div className="mb-3">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
            Navigation
          </h3>
        </div>
        <Navigation variant="sidebar" />
      </div>

      {/* Search History Section - Flexible, scrollable with improved styling */}
      <div className="flex-1 px-6 py-5 overflow-y-auto bg-white">
        <div className="mb-3">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
            Recent Searches
          </h3>
        </div>
        <SearchHistory variant="sidebar" onHistoryItemClick={onHistoryItemClick} />
      </div>

      {/* New Search Button - At bottom, fixed height with prominent styling */}
      <div className="flex-shrink-0 p-6 border-t border-gray-100 bg-gradient-to-t from-gray-50 to-white">
        <NewSearchButton onNewSearch={onNewSearch} />
      </div>
    </div>
  );
}
