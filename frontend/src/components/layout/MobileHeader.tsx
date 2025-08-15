import React, { useState } from 'react';
import { AppLogo, UserProfile, NewSearchButton } from '../ui';
import { SearchHistory } from '../features';

/**
 * Mobile header component with hamburger menu
 * Only visible on mobile devices for responsive design
 * Uses modular subcomponents for better organization and reusability
 */
export default function MobileHeader() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <div className="lg:hidden bg-white border-b border-gray-200 px-4 py-3">
      <div className="flex items-center justify-between">
        {/* Logo */}
        <AppLogo variant="mobile" showSubtitle={false} />

        {/* Hamburger Menu Button */}
        <button
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className="p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200"
        >
          <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      {/* Mobile Menu Overlay */}
      {isMenuOpen && (
        <div className="absolute top-full left-0 right-0 bg-white border-b border-gray-200 shadow-lg z-50">
          <div className="p-4 space-y-4">
            {/* App Title - At top */}
            <div className="pb-4 border-b border-gray-200">
              <AppLogo variant="sidebar" showSubtitle={true} />
            </div>

            {/* User Profile */}
            <UserProfile variant="mobile" />

            {/* Search History */}
            <SearchHistory variant="mobile" />

            {/* New Search Button - At bottom */}
            <div className="pt-4 border-t border-gray-200">
              <NewSearchButton variant="mobile" />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
