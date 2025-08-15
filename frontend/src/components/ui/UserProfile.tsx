import React from 'react';
import { toast } from 'react-hot-toast';

interface UserProfileProps {
  variant?: 'sidebar' | 'mobile';
}

/**
 * UserProfile component displaying user information and login button
 * Can be used in sidebar, mobile header, or other UI areas
 */
export default function UserProfile({ variant = 'sidebar' }: UserProfileProps) {
  const handleComingSoon = () => {
    toast('Feature Coming Soon!', {
      duration: 2000,
      position: 'bottom-right',
      style: {
        background: '#363636',
        color: '#fff',
      },
    });
  };

  const isMobile = variant === 'mobile';

  return (
    <div className={`flex items-center space-x-3 ${isMobile ? 'pb-4 border-b border-gray-200' : ''}`}>
      {/* User Avatar */}
      <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
        <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      </div>
      
      {/* User Info */}
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-900">Guest User</p>
        <p className="text-xs text-gray-500">Free Plan</p>
      </div>
      
      {/* Login Button */}
      <button
        onClick={handleComingSoon}
        className="text-sm text-blue-600 hover:text-blue-700 font-medium transition-colors duration-200"
      >
        Log In
      </button>
    </div>
  );
}
