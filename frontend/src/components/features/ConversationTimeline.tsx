import React, { useEffect, useRef } from "react";
import TimelineEntry, { ConversationEntry } from "./TimelineEntry";

interface ConversationTimelineProps {
  conversationHistory: ConversationEntry[];
  onNewSearch: () => void;
  error?: string;
  isLoading?: boolean;
  currentQuery?: string;
  scrollContainer?:
    | React.RefObject<HTMLElement>
    | React.MutableRefObject<HTMLElement | null>;
  scrollOffset?: number;
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
  scrollContainer,
  scrollOffset = 20,
}: ConversationTimelineProps) {
  const currentQuestionRef = useRef<HTMLDivElement>(null);
  const lastScrolledQueryRef = useRef<string | null>(null);
  const topBarRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isLoading || !currentQuery) {
      lastScrolledQueryRef.current = null;
      return;
    }

    if (lastScrolledQueryRef.current === currentQuery) {
      console.debug("[ConversationTimeline] Scroll already attempted for query", {
        currentQuery,
      });
      return;
    }

    lastScrolledQueryRef.current = currentQuery;

    const timeoutId = window.setTimeout(() => {
      const target = currentQuestionRef.current;

      if (!target) {
        console.warn("[ConversationTimeline] No target element for scroll", {
          currentQuery,
        });
        return;
      }

      const container = scrollContainer?.current ?? document.documentElement;
      const isDocumentContainer =
        container === document.documentElement || container === document.body;
      const topBarHeight = topBarRef.current?.offsetHeight ?? 0;
      const totalOffset = scrollOffset + topBarHeight;

      console.info("[ConversationTimeline] Initiating scroll on submission", {
        currentQuery,
        isDocumentContainer,
        scrollOffset,
        topBarHeight,
        totalOffset,
      });

      target.scrollIntoView({ behavior: "smooth", block: "start" });

      const performManualScroll = () => {
        let position = 0;

        if (isDocumentContainer) {
          const targetRect = target.getBoundingClientRect();
          const scrollTop =
            window.pageYOffset || document.documentElement.scrollTop;
          position = Math.max(targetRect.top + scrollTop - totalOffset, 0);
          console.debug("[ConversationTimeline] Manual document scroll", {
            position,
          });
          window.scrollTo({ top: position, behavior: "smooth" });
        } else {
          const containerRect = container.getBoundingClientRect();
          const targetRect = target.getBoundingClientRect();
          position =
            targetRect.top - containerRect.top + container.scrollTop - totalOffset;
          console.debug("[ConversationTimeline] Manual container scroll", {
            position,
          });
          container.scrollTo({ top: Math.max(position, 0), behavior: "smooth" });
        }
      };

      window.requestAnimationFrame(() => {
        performManualScroll();
        window.setTimeout(performManualScroll, 160);
      });
    }, 100);

    return () => window.clearTimeout(timeoutId);
  }, [isLoading, currentQuery, scrollContainer, scrollOffset]);

  useEffect(() => {
    if (!isLoading) {
      lastScrolledQueryRef.current = null;
    }
  }, [isLoading]);

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
    <div data-conversation-container className="flex-1 relative">
      <div
        ref={topBarRef}
        className="sticky top-0 z-10 w-full bg-white dark:bg-gray-900 shadow-sm"
      >
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

      <div className="px-4 lg:px-8 pt-4 pb-8">
        <div className="max-w-4xl mx-auto">
          <div className="space-y-0">
            {conversationHistory.map((entry, index) => {
              const isLastEntry = index === conversationHistory.length - 1;

              return (
                <TimelineEntry
                  key={index}
                  entry={entry}
                  isLast={!isLoading && isLastEntry}
                  isLoading={false}
                  currentQuery={currentQuery}
                />
              );
            })}

            {isLoading && currentQuery && (
              <TimelineEntry
                ref={currentQuestionRef}
                entry={undefined}
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
