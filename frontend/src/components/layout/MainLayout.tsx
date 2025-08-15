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
  return (
    <div className="h-screen bg-gray-50">
      {/* Mobile Header - Only visible on mobile */}
      <MobileHeader />
      
      <div className="flex h-full">
        {/* Left Sidebar - Hidden on mobile, visible on lg+ */}
        <div className="hidden lg:block">
          <Sidebar />
        </div>
        
        {/* Main Content Area - Takes remaining space */}
        <main className="flex-1 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
