import React from 'react';
import Sidebar from './Sidebar';
import MobileHeader from './MobileHeader';

interface MainLayoutProps {
  children: React.ReactNode;
}

/**
 * Main layout component that provides the overall page structure
 * Includes sidebar, mobile header, and main content area
 * Supports both light and dark themes
 */
export default function MainLayout({ children }: MainLayoutProps) {
  const handleNewSearch = () => {
    // This will be handled by MainContent
    console.log('New search requested');
  };

  const handleHistoryItemClick = (query: string) => {
    console.log('History item clicked:', query);
  };

  return (
    <div className="h-screen bg-gray-50 flex flex-col dark:bg-gray-900">
      <div className="lg:hidden">
        <MobileHeader />
      </div>
      <div className="flex flex-1 overflow-hidden">
        <div className="hidden lg:block lg:w-80 lg:flex-shrink-0">
          <Sidebar onNewSearch={handleNewSearch} onHistoryItemClick={handleHistoryItemClick} />
        </div>
        <main className="flex-1 overflow-auto relative">
          {children}
        </main>
      </div>
    </div>
  );
}
