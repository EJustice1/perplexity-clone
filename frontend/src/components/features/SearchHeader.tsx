import React from "react";

/**
 * SearchHeader component displaying the main search page title and description
 */
export default function SearchHeader() {
  return (
    <div className="text-center mb-8">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">Ask anything</h1>
      <p className="text-lg text-gray-600">
        Get instant answers to your questions with AI-powered search
      </p>
    </div>
  );
}
