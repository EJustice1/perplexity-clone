import React from 'react';
import Sidebar from './Sidebar';
import MobileHeader from './MobileHeader';

interface MainLayoutProps {
  children: React.ReactNode;
}

/**
 * Main layout component that establishes the two-panel structure
 * Left sidebar (fixed) and main content area (flexible)
 * Includes responsive design with mobile header
 */
export default function MainLayout({ children }: MainLayoutProps) {
  const handleNewSearch = () => {
    // This will be handled by the MainContent component
  };

  const handleHistoryItemClick = (query: string) => {
    // This will trigger a new search with the selected query
    // The actual search functionality will be implemented in the next phase
    console.log('History item clicked:', query);
  };

  return (
    <div className="h-screen bg-gray-50 flex flex-col">
      {/* Mobile Header - Only visible on mobile, fixed at top */}
      <div className="lg:hidden">
        <MobileHeader />
      </div>
      
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar - Hidden on mobile, visible on lg+, fixed width */}
        <div className="hidden lg:block lg:w-80 lg:flex-shrink-0">
          <Sidebar 
            onNewSearch={handleNewSearch}
            onHistoryItemClick={handleHistoryItemClick}
          />
        </div>
        
        {/* Main Content Area - Takes remaining space, scrollable */}
        <main className="flex-1 overflow-auto relative">
          {children}
        </main>
      </div>
    </div>
  );
}
