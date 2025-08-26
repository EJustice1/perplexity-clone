import React from "react";

interface Source {
  title: string;
  url: string;
  snippet: string;
  source?: string;
}

interface SourcesListProps {
  sources: Source[];
  className?: string;
}

/**
 * Clean sources list component with proper link handling
 */
export const SourcesList: React.FC<SourcesListProps> = ({
  sources,
  className = "",
}) => {
  if (!sources || sources.length === 0) {
    return (
      <div
        className={`text-center py-8 text-gray-500 dark:text-gray-400 ${className}`}
      >
        <p>No sources available</p>
      </div>
    );
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {sources.map((source, index) => (
        <div
          key={index}
          className="flex items-start space-x-4 p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-200 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
        >
          {/* Source number */}
          <div className="flex-shrink-0 w-8 h-8 bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center text-sm font-semibold text-blue-600 dark:text-blue-400">
            {index + 1}
          </div>

          {/* Source content */}
          <div className="flex-1 min-w-0">
            <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-1">
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors duration-200 hover:underline"
              >
                {source.title}
              </a>
            </h4>

            <p className="text-xs text-gray-500 dark:text-gray-400 mb-2 truncate">
              {new URL(source.url).hostname}
            </p>

            <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed line-clamp-3">
              {source.snippet}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default SourcesList;
