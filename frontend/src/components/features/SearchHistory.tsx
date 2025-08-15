import React from 'react';
import { toast } from 'react-hot-toast';

interface SearchHistoryProps {
  variant?: 'sidebar' | 'mobile';
}

/**
 * SearchHistory component displaying a list of recent searches
 * Supports different variants for sidebar and mobile layouts
 */
export default function SearchHistory({ variant = 'sidebar' }: SearchHistoryProps) {
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

  const searchItems = [
    "What is artificial intelligence?",
    "How to build a React app",
    "Best practices for TypeScript",
    "Machine learning fundamentals",
    "Web development trends 2024"
  ];

  const mobileItems = [
    "What is AI?",
    "React best practices",
    "TypeScript tips"
  ];

  const items = variant === 'mobile' ? mobileItems : searchItems;

  return (
    <div>
      <h2 className="text-sm font-medium text-gray-500 uppercase tracking-wider mb-4">
        {variant === 'mobile' ? 'Recent Searches' : 'Search History'}
      </h2>
      <div className="space-y-2">
        {items.map((item, index) => (
          <button
            key={index}
            onClick={handleComingSoon}
            className="w-full text-left p-3 rounded-lg hover:bg-gray-100 transition-colors duration-200 text-gray-700 hover:text-gray-900"
          >
            <div className="flex items-center space-x-3">
              <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <span className="text-sm truncate">{item}</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
