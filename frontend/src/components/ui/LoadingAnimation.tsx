import React from "react";

interface LoadingAnimationProps {
  size?: "sm" | "md" | "lg";
  className?: string;
}

/**
 * Loading animation component with different sizes
 * Shows a pulsing dot animation for loading states
 */
export default function LoadingAnimation({ size = "md", className = "" }: LoadingAnimationProps) {
  const sizeClasses = {
    sm: "w-2 h-2",
    md: "w-3 h-3",
    lg: "w-4 h-4",
  };

  return (
    <div className={`flex items-center space-x-1 ${className}`} data-testid="loading-animation">
      <div
        className={`${sizeClasses[size]} bg-blue-500 dark:bg-blue-400 rounded-full animate-pulse`}
        style={{ animationDelay: "0ms" }}
      />
      <div
        className={`${sizeClasses[size]} bg-blue-500 dark:bg-blue-400 rounded-full animate-pulse`}
        style={{ animationDelay: "150ms" }}
      />
      <div
        className={`${sizeClasses[size]} bg-blue-500 dark:bg-blue-400 rounded-full animate-pulse`}
        style={{ animationDelay: "300ms" }}
      />
    </div>
  );
}
