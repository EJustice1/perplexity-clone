import React, { useEffect, useRef } from "react";
import TimelineEntry, { ConversationEntry } from "./TimelineEntry";

interface ConversationTimelineProps {
  conversationHistory: ConversationEntry[];
  onNewSearch: () => void;
  error?: string;
  isLoading?: boolean;
  currentQuery?: string;
}

/**
 * Conversation timeline component that displays search history as a continuous chain
 * Shows original question at top, most recent at bottom with loading animation for current question
 * Supports both light and dark themes
 */
export default function ConversationTimeline({
  conversationHistory,
  onNewSearch,
  error,
  isLoading,
  currentQuery,
}: ConversationTimelineProps) {
  const currentQuestionRef = useRef<HTMLDivElement>(null);
  const stickyHeaderRef = useRef<HTMLDivElement>(null);

  // Simple scroll to top when loading starts (question appears)
  useEffect(() => {
    if (isLoading && currentQuery) {
      // Use setTimeout to ensure DOM is fully rendered before scrolling
      setTimeout(() => {
        if (currentQuestionRef.current) {
          console.log('Attempting to scroll, element found:', currentQuestionRef.current);
          
          try {
            // Find the actual scrollable container (main element with overflow-auto)
            const scrollableContainer = currentQuestionRef.current?.closest('main[class*="overflow-auto"]') || 
                                     currentQuestionRef.current?.closest('main') ||
                                     document.documentElement;
            
            // Get the element's absolute position using offsetTop (not affected by current scroll)
            const elementAbsoluteTop = currentQuestionRef.current.offsetTop;
            
            // Get sticky header height
            const headerHeight = stickyHeaderRef.current?.offsetHeight || 72;
            const padding = 20; // Additional padding below header
            
            // Calculate final scroll position (absolute position minus header and padding)
            const scrollPosition = elementAbsoluteTop - headerHeight - padding;
            
            console.log('Scrolling to position below sticky header:', {
              elementAbsoluteTop,
              headerHeight,
              padding,
              scrollPosition,
              scrollableContainer: scrollableContainer.tagName
            });
            
            // Scroll the correct container
            if (scrollableContainer === document.documentElement) {
              // If it's the document, use scrollTo for smooth behavior
              document.documentElement.scrollTo({
                top: scrollPosition,
                behavior: 'smooth'
              });
            } else {
              // If it's a main element, scroll that container smoothly
              scrollableContainer.scrollTo({
                top: scrollPosition,
                behavior: 'smooth'
              });
            }
            
          } catch (error) {
            console.error('Scroll error:', error);
          }
        } else {
          console.log('Element ref not found');
        }
      }, 100); // Small delay to ensure DOM is ready
    }
  }, [isLoading, currentQuery]);

  if (conversationHistory.length === 0 && !isLoading) {
    return null;
  }

  // Show error if there is one
  if (error) {
    return (
      <div className="flex-1 px-4 lg:px-8 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center max-w-2xl">
            <div className="w-16 h-16 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg
                className="w-8 h-8 text-red-600 dark:text-red-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Something went wrong
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">{error}</p>
            <button
              onClick={onNewSearch}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors duration-200"
            >
              Try again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div 
      data-conversation-container
      className="flex-1 relative"
    >
      {/* Sticky New Search Button - Full Width Background */}
      <div ref={stickyHeaderRef} className="sticky top-0 z-10 w-full bg-white dark:bg-gray-900 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 lg:px-8 py-4">
          <div className="text-right">
            <button
              onClick={onNewSearch}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg transition-colors duration-200 font-medium"
            >
              ← New Search
            </button>
          </div>
        </div>
      </div>

      {/* Conversation Timeline - Continuous Chain */}
      <div className="px-4 lg:px-8 pt-4 pb-8">
        <div className="max-w-4xl mx-auto">
          <div className="space-y-0">
            {/* Show conversation history */}
            {conversationHistory.map((entry, index) => (
              <TimelineEntry 
                key={index} 
                entry={entry} 
                isLast={!isLoading && index === conversationHistory.length - 1}
                isLoading={false}
                currentQuery={currentQuery}
              />
            ))}
            
            {/* Show loading animation for current question if searching */}
            {isLoading && currentQuery && (
              <TimelineEntry 
                ref={currentQuestionRef} 
                entry={undefined} // Pass undefined for the loading entry
                isLast={true}
                isLoading={true}
                currentQuery={currentQuery}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
