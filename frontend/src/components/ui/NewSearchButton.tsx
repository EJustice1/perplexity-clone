import React from 'react';
import { toast } from 'react-hot-toast';

/**
 * NewSearchButton component for starting new searches
 * Can be used in sidebar and mobile layouts
 */
export default function NewSearchButton() {
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

  return (
    <button
      onClick={handleComingSoon}
      className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
    >
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
      </svg>
      <span>New Search</span>
    </button>
  );
}
