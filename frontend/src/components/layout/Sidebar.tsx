import React from 'react';
import { UserProfile, AppLogo, NewSearchButton } from '../ui';
import { SearchHistory } from '../features';

/**
 * Sidebar component containing navigation and user interface elements
 * Uses modular subcomponents for better organization and reusability
 */
export default function Sidebar() {
  return (
    <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
      {/* App Title - At top */}
      <div className="p-6 border-b border-gray-200">
        <AppLogo variant="sidebar" showSubtitle={true} />
      </div>

      {/* User Profile Section */}
      <div className="p-6 border-b border-gray-200">
        <UserProfile variant="sidebar" />
      </div>

      {/* Search History Section */}
      <div className="flex-1 px-6 py-4">
        <SearchHistory variant="sidebar" />
      </div>

      {/* New Search Button - At bottom */}
      <div className="p-6 border-t border-gray-200">
        <NewSearchButton />
      </div>
    </div>
  );
}
