"use client";

import { Toaster } from 'react-hot-toast';
import MainLayout from '../../components/layout/MainLayout';
import { Help } from '../../components/features';

/**
 * Help page - FAQ and support information
 * Uses the existing Help component with proper layout
 */
export default function HelpPage() {
  return (
    <>
      <MainLayout>
        <div className="min-h-full bg-gray-50">
          <Help />
        </div>
      </MainLayout>
      
      {/* Toast notifications */}
      <Toaster />
    </>
  );
}
