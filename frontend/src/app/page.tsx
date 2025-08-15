"use client";

import { Toaster } from 'react-hot-toast';
import MainLayout from '../components/layout/MainLayout';
import MainContent from '../components/layout/MainContent';

/**
 * Main page component implementing the Perplexity-style UI
 * Features a two-panel layout with sidebar and main content area
 */
export default function Home() {
  return (
    <>
      <MainLayout>
        <MainContent />
      </MainLayout>
      
      {/* Toast notifications for "Coming Soon" features */}
      <Toaster />
    </>
  );
}
