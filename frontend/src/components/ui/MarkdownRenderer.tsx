import React, { useEffect, useState } from "react";
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
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    // Check for dark mode
    const checkDarkMode = () => {
      const isDarkMode =
        document.documentElement.classList.contains("dark") ||
        window.matchMedia("(prefers-color-scheme: dark)").matches;
      setIsDark(isDarkMode);
    };

    checkDarkMode();

    // Listen for theme changes
    const observer = new MutationObserver(checkDarkMode);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"],
    });

    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    mediaQuery.addEventListener("change", checkDarkMode);

    return () => {
      observer.disconnect();
      mediaQuery.removeEventListener("change", checkDarkMode);
    };
  }, []);

  // Production-ready color scheme following UI/UX best practices
  const colors = {
    // Borders: Subtle but visible, following accessibility guidelines
    border: isDark ? "#4b5563" : "#e5e7eb",

    // Header: Distinct background with proper contrast
    headerBg: isDark ? "#1f2937" : "#f8fafc",
    headerText: isDark ? "#f9fafb" : "#0f172a",

    // Cells: Clean background with excellent readability
    cellBg: isDark ? "#111827" : "#ffffff",
    cellText: isDark ? "#e2e8f0" : "#1e293b",

    // Hover states for better interactivity
    hoverBg: isDark ? "#374151" : "#f1f5f9",
  };
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
                className="markdown-table w-full border-collapse"
                style={{
                  border: `1px solid ${colors.border}`,
                  width: "100%",
                  margin: "1.5rem 0",
                  backgroundColor: colors.cellBg,
                  borderRadius: "8px",
                  overflow: "hidden",
                }}
              >
                {children}
              </table>
            </div>
          ),
          // Production-ready table header styling
          th: ({ children, ...props }) => (
            <th
              {...props}
              style={{
                border: `1px solid ${colors.border}`,
                padding: "16px 20px",
                backgroundColor: colors.headerBg,
                fontWeight: "600",
                textAlign: "left",
                fontSize: "0.875rem",
                color: colors.headerText,
                borderBottom: `2px solid ${colors.border}`,
              }}
            >
              {children}
            </th>
          ),
          // Production-ready table cell styling with alternating rows
          td: ({ children, ...props }) => (
            <td
              {...props}
              style={{
                border: `1px solid ${colors.border}`,
                padding: "16px 20px",
                fontSize: "0.875rem",
                color: colors.cellText,
                lineHeight: "1.6",
                backgroundColor: colors.cellBg,
                transition: "background-color 0.15s ease-in-out",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = colors.hoverBg;
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = colors.cellBg;
              }}
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
