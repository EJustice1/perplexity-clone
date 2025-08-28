import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

/**
 * Clean markdown renderer with table gridlines support
 * Uses react-markdown with GitHub Flavored Markdown for tables
 */
export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({
  content,
  className = "",
}) => {


  return (
    <div className={`markdown-content max-w-none ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Production-ready table styling with proper light/dark mode
          table: ({ children, ...props }) => (
            <div className="overflow-x-auto my-6">
              <table
                {...props}
                className="markdown-table w-full border-collapse border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 rounded-lg overflow-hidden"
              >
                {children}
              </table>
            </div>
          ),
          // Production-ready table header styling
          th: ({ children, ...props }) => (
            <th
              {...props}
              className="border border-gray-300 dark:border-gray-600 px-5 py-4 bg-gray-50 dark:bg-gray-700 font-semibold text-left text-sm text-gray-900 dark:text-gray-100 border-b-2 border-gray-300 dark:border-gray-600"
            >
              {children}
            </th>
          ),
          // Production-ready table cell styling with alternating rows
          td: ({ children, ...props }) => (
            <td
              {...props}
              className="border border-gray-300 dark:border-gray-600 px-5 py-4 text-sm text-gray-900 dark:text-gray-100 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-150"
            >
              {children}
            </td>
          ),
          // Custom link styling with proper target handling
          a: ({ href, children, ...props }) => (
            <a
              {...props}
              href={href}
              target={href?.startsWith("http") ? "_blank" : undefined}
              rel={href?.startsWith("http") ? "noopener noreferrer" : undefined}
              className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 underline transition-colors duration-200"
            >
              {children}
            </a>
          ),
          // Custom code block styling
          code: ({ children, ...props }) => {
            // Check if it's inline code by checking if it's inside a paragraph
            const isInline =
              typeof children === "string" && !children.includes("\n");
            return isInline ? (
              <code
                {...props}
                className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-2 py-1 rounded text-sm font-mono"
              >
                {children}
              </code>
            ) : (
              <code
                {...props}
                className="block bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 p-4 rounded-lg text-sm font-mono overflow-x-auto"
              >
                {children}
              </code>
            );
          },
          // Custom blockquote styling
          blockquote: ({ children, ...props }) => (
            <blockquote
              {...props}
              className="border-l-4 border-blue-500 pl-4 italic text-gray-600 dark:text-gray-400 my-4"
            >
              {children}
            </blockquote>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer;
