import React from 'react';

/**
 * ResultDisplay component showing the area where search results will appear
 * Currently displays a placeholder as per Part 1 Stage 1 requirements
 */
export default function ResultDisplay() {
  return (
    <div className="px-8 pb-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-2xl border border-gray-200 p-8 text-center">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Ready to search
          </h3>
          <p className="text-gray-600">
            Type your question above to get started
          </p>
        </div>
      </div>
    </div>
  );
}
