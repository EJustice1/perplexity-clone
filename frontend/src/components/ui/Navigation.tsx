import React from "react";
import { useRouter, usePathname } from "next/navigation";

interface NavigationProps {
  variant?: "sidebar" | "mobile";
}

/**
 * Navigation component following industry standard web layouts
 * Uses proper spacing, typography, and visual hierarchy
 * Now navigates to actual pages and highlights current page
 * Supports both light and dark themes
 */
export default function Navigation({ variant = "sidebar" }: NavigationProps) {
  const router = useRouter();
  const pathname = usePathname();

  const navigationItems = [
    {
      name: "Search",
      href: "/",
      icon: (
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      ),
    },
    {
      name: "Profile",
      href: "/profile",
      icon: (
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
          />
        </svg>
      ),
    },
    {
      name: "Subscribed Topics",
      href: "/topics",
      icon: (
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M3 7l9-4 9 4-9 4-9-4z"
          />
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M3 12l9 4 9-4"
          />
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M3 17l9 4 9-4"
          />
        </svg>
      ),
    },
  ];

  const handleNavigationClick = (item: (typeof navigationItems)[0]) => {
    if (item.href === pathname) {
      // Already on this page
      return;
    }

    // Navigate to the page
    router.push(item.href);
  };

  return (
    <nav
      className={`${variant === "mobile" ? "space-y-1" : "space-y-1"}`}
      role="navigation"
      aria-label="Main navigation"
    >
      {navigationItems.map((item) => {
        const isActive = pathname === item.href;

        return (
          <button
            key={item.name}
            onClick={() => handleNavigationClick(item)}
            className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-left transition-all duration-200 ${
              isActive
                ? "bg-blue-50 text-blue-700 border border-blue-200 shadow-sm dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-700"
                : "text-gray-700 hover:bg-gray-100 hover:text-gray-900 hover:shadow-sm dark:text-gray-300 dark:hover:bg-gray-800 dark:hover:text-gray-100"
            }`}
            aria-current={isActive ? "page" : undefined}
          >
            <span
              className={`flex-shrink-0 ${isActive ? "text-blue-600 dark:text-blue-400" : "text-gray-500 dark:text-gray-400"}`}
            >
              {item.icon}
            </span>
            <span
              className={`font-medium ${variant === "mobile" ? "text-sm" : "text-sm"}`}
            >
              {item.name}
            </span>
          </button>
        );
      })}
    </nav>
  );
}
