import React from 'react';
import { toast } from 'react-hot-toast';

interface NavigationProps {
  variant?: 'sidebar' | 'mobile';
}

/**
 * Navigation component following industry standard web layouts
 * Uses proper spacing, typography, and visual hierarchy
 */
export default function Navigation({ variant = 'sidebar' }: NavigationProps) {
  const navigationItems = [
    {
      name: 'Home',
      href: '/',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
      )
    },
    {
      name: 'Profile',
      href: '/profile',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      )
    },
    {
      name: 'Settings',
      href: '/settings',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      )
    },
    {
      name: 'Help & Support',
      href: '/help',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      )
    }
  ];

  const handleNavigationClick = (item: typeof navigationItems[0]) => {
    if (item.href === '/') {
      // Home is already active
      return;
    }
    
    toast(`${item.name} page will be implemented in the next phase!`, {
      duration: 3000,
      position: 'top-center',
      style: {
        background: '#363636',
        color: '#fff',
      },
    });
  };

  const isMobile = variant === 'mobile';

  return (
    <nav className={`${isMobile ? 'space-y-1' : 'space-y-1'}`} role="navigation" aria-label="Main navigation">
      {navigationItems.map((item) => (
        <button
          key={item.name}
          onClick={() => handleNavigationClick(item)}
          className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-left transition-all duration-200 ${
            item.href === '/' 
              ? 'bg-blue-50 text-blue-700 border border-blue-200 shadow-sm' 
              : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900 hover:shadow-sm'
          }`}
          aria-current={item.href === '/' ? 'page' : undefined}
        >
          <span className="flex-shrink-0 text-gray-500">{item.icon}</span>
          <span className={`font-medium ${isMobile ? 'text-sm' : 'text-sm'}`}>
            {item.name}
          </span>
        </button>
      ))}
    </nav>
  );
}
