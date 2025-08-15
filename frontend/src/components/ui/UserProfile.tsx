import React, { useState } from 'react';
import { toast } from 'react-hot-toast';
import { LoginModal } from './index';

interface UserProfileProps {
  variant?: 'sidebar' | 'mobile';
}

/**
 * UserProfile component displaying user information and login functionality
 * Now uses a centered modal for login
 */
export default function UserProfile({ variant = 'sidebar' }: UserProfileProps) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);

  const handleLogout = () => {
    setIsLoggedIn(false);
    toast('Logout functionality will be implemented in the next phase!', {
      duration: 3000,
      position: 'top-center',
      style: {
        background: '#363636',
        color: '#fff',
      },
    });
  };

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  const isMobile = variant === 'mobile';

  if (isLoggedIn) {
    return (
      <div className={`flex items-center space-x-3 ${isMobile ? 'pb-4 border-b border-gray-200' : ''}`}>
        <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
          <span className="text-white font-bold text-sm">U</span>
        </div>
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-900">User</p>
          <p className="text-xs text-gray-500">Premium Plan</p>
        </div>
        <button
          onClick={handleLogout}
          className="text-sm text-red-600 hover:text-red-700 font-medium transition-colors duration-200"
        >
          Log Out
        </button>
      </div>
    );
  }

  return (
    <>
      <div className={`flex items-center space-x-3 ${isMobile ? 'pb-4 border-b border-gray-200' : ''}`}>
        <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
          <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-900">Guest User</p>
          <p className="text-xs text-gray-500">Free Plan</p>
        </div>
        <button
          onClick={() => setShowLoginModal(true)}
          className="text-sm text-blue-600 hover:text-blue-700 font-medium transition-colors duration-200"
        >
          Log In
        </button>
      </div>

      {/* Login Modal */}
      <LoginModal
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
        onLoginSuccess={handleLoginSuccess}
      />
    </>
  );
}
