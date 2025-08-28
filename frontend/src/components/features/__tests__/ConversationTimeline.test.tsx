import React from 'react';
import { render, screen } from '@testing-library/react';

// Mock the MarkdownRenderer component to avoid Jest issues
jest.mock('../../ui/MarkdownRenderer', () => {
  return function MockMarkdownRenderer({ content }: { content: string }) {
    return <div data-testid="markdown-renderer">{content}</div>;
  };
});

import ConversationTimeline from '../ConversationTimeline';

// Mock the scrollIntoView method
const mockScrollIntoView = jest.fn();
Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', {
  value: mockScrollIntoView,
  writable: true,
});

// Mock the querySelector method
const mockQuerySelector = jest.fn();
Object.defineProperty(document, 'querySelector', {
  value: mockQuerySelector,
  writable: true,
});

describe('ConversationTimeline', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockScrollIntoView.mockClear();
    mockQuerySelector.mockClear();
  });

  const mockConversationHistory = [
    {
      query: 'What is quantum computing?',
      sources: [],
      extractedContent: [],
      timestamp: new Date('2024-01-01T10:00:00Z'),
    },
  ];

  it('renders conversation history', () => {
    render(
      <ConversationTimeline
        conversationHistory={mockConversationHistory}
        onNewSearch={jest.fn()}
        isLoading={false}
      />
    );

    expect(screen.getByText('What is quantum computing?')).toBeInTheDocument();
  });

  it('shows loading state with current query', () => {
    render(
      <ConversationTimeline
        conversationHistory={mockConversationHistory}
        onNewSearch={jest.fn()}
        isLoading={true}
        currentQuery="What is AI?"
      />
    );

    expect(screen.getByText('What is AI?')).toBeInTheDocument();
    expect(screen.getByText('Searching for answers...')).toBeInTheDocument();
  });

  it('shows error state', () => {
    const errorMessage = 'Something went wrong';
    render(
      <ConversationTimeline
        conversationHistory={mockConversationHistory}
        onNewSearch={jest.fn()}
        error={errorMessage}
        isLoading={false}
      />
    );

    expect(screen.getByRole('heading', { name: 'Something went wrong' })).toBeInTheDocument();
    expect(screen.getAllByText(errorMessage)).toHaveLength(2); // Heading and paragraph
    expect(screen.getByText('Try again')).toBeInTheDocument();
  });

  it('calls onNewSearch when new search button is clicked', () => {
    const mockOnNewSearch = jest.fn();
    render(
      <ConversationTimeline
        conversationHistory={mockConversationHistory}
        onNewSearch={mockOnNewSearch}
        isLoading={false}
      />
    );

    screen.getByText('← New Search').click();
    expect(mockOnNewSearch).toHaveBeenCalledTimes(1);
  });

  it('renders nothing when no conversation history and not loading', () => {
    const { container } = render(
      <ConversationTimeline
        conversationHistory={[]}
        onNewSearch={jest.fn()}
        isLoading={false}
      />
    );

    expect(container.firstChild).toBeNull();
  });
});
