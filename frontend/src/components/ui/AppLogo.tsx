import React from 'react';

interface AppLogoProps {
  variant?: 'sidebar' | 'mobile';
  showSubtitle?: boolean;
}

/**
 * AppLogo component displaying the application logo and title
 * Supports different variants for sidebar and mobile header
 */
export default function AppLogo({ variant = 'sidebar', showSubtitle = true }: AppLogoProps) {
  const isSidebar = variant === 'sidebar';
  
  return (
    <div className={`flex items-center space-x-3 ${isSidebar ? 'justify-center' : ''}`}>
      {/* Logo Icon */}
      <div className={`bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center ${
        isSidebar ? 'w-12 h-12' : 'w-8 h-8'
      }`}>
        <span className={`text-white font-bold ${isSidebar ? 'text-xl' : 'text-lg'}`}>P</span>
      </div>
      
      {/* App Title */}
      <div className={isSidebar ? 'text-center' : ''}>
        <h1 className={`font-semibold text-gray-900 ${isSidebar ? 'text-xl' : 'text-lg'}`}>
          Perplexity Clone
        </h1>
        {showSubtitle && isSidebar && (
          <p className="text-sm text-gray-500 mt-1">AI-Powered Search</p>
        )}
      </div>
    </div>
  );
}
