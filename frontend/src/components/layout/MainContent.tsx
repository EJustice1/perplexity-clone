import React, { useState } from "react";
import { useSearch } from "../../hooks";
import {
  SearchInput,
  SearchSuggestions,
  ConversationTimeline,
  FollowUpSearch,
} from "../features";

/**
 * Main content component that manages search functionality
 * Shows either initial search page or results page based on search state
 * Supports both light and dark themes
 */
export default function MainContent() {
  const {
    isLoading,
    error,
    hasSearched,
    search,
    clearResults,
    conversationHistory,
  } = useSearch();
  const [suggestionQuery, setSuggestionQuery] = useState<string | undefined>();
  const [shouldAutoSearch, setShouldAutoSearch] = useState(false);

  const handleSearch = async (query: string) => {
    await search(query);
  };

  const handleRecommendationClick = (query: string) => {
    setSuggestionQuery(query);
    setShouldAutoSearch(true);
    // Reset auto-search flag after a short delay
    setTimeout(() => {
      setShouldAutoSearch(false);
    }, 100);
  };

  const handleNewSearch = () => {
    clearResults();
    setSuggestionQuery(undefined);
    setShouldAutoSearch(false);
  };

  // Show initial search page when no search has been performed
  if (!hasSearched) {
    return (
      <div className="min-h-full flex flex-col bg-gray-50 dark:bg-gray-900">
        <SearchInput
          onSearch={handleSearch}
          isLoading={isLoading}
          externalQuery={suggestionQuery}
          shouldAutoSearch={shouldAutoSearch}
        />
        <SearchSuggestions
          onSearch={handleRecommendationClick}
          isLoading={isLoading}
        />
      </div>
    );
  }

  // Show results page when search has been performed
  return (
    <div className="relative min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Conversation Timeline */}
      <div className="pb-24">
        <ConversationTimeline
          conversationHistory={conversationHistory}
          onNewSearch={handleNewSearch}
          error={error}
          isLoading={isLoading}
        />
      </div>

      {/* Bottom Search Bar for Follow-up Questions - Fixed to viewport */}
      <FollowUpSearch onSearch={handleSearch} isLoading={isLoading} />
    </div>
  );
}
