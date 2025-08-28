import React from 'react';
import { render, screen } from '@testing-library/react';
import LoadingAnimation from '../LoadingAnimation';

describe('LoadingAnimation', () => {
  it('renders with default size', () => {
    render(<LoadingAnimation />);
    const dots = screen.getAllByRole('generic').filter(el => 
      el.className.includes('bg-blue-500') || el.className.includes('bg-blue-400')
    );
    expect(dots).toHaveLength(3);
  });

  it('renders with small size', () => {
    render(<LoadingAnimation size="sm" />);
    const dots = screen.getAllByRole('generic').filter(el => 
      el.className.includes('w-2 h-2')
    );
    expect(dots).toHaveLength(3);
  });

  it('renders with large size', () => {
    render(<LoadingAnimation size="lg" />);
    const dots = screen.getAllByRole('generic').filter(el => 
      el.className.includes('w-4 h-4')
    );
    expect(dots).toHaveLength(3);
  });

  it('applies custom className', () => {
    render(<LoadingAnimation className="custom-class" />);
    const container = screen.getByTestId('loading-animation');
    expect(container).toHaveClass('custom-class');
  });
});
