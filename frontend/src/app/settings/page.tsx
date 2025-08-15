"use client";

import { Toaster } from 'react-hot-toast';
import MainLayout from '../../components/layout/MainLayout';
import { Settings } from '../../components/features';

/**
 * Settings page - User preferences and account settings
 * Uses the existing Settings component with proper layout
 */
export default function SettingsPage() {
  return (
    <>
      <MainLayout>
        <div className="min-h-full bg-gray-50">
          <Settings />
        </div>
      </MainLayout>
      
      {/* Toast notifications */}
      <Toaster />
    </>
  );
}
