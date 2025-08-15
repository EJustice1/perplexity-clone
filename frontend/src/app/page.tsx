"use client";

import { Toaster } from 'react-hot-toast';
import MainLayout from '../components/layout/MainLayout';
import MainContent from '../components/layout/MainContent';

/**
 * Main search page - Home page with search functionality
 * Client component to support theme switching
 */
export default function HomePage() {
  return (
    <>
      <MainLayout>
        <MainContent />
      </MainLayout>
      
      {/* Toast notifications */}
      <Toaster />
    </>
  );
}
