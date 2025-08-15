"use client";

import { Toaster } from 'react-hot-toast';
import MainLayout from '../../components/layout/MainLayout';
import { Profile } from '../../components/features';

/**
 * Profile page - User profile information and editing
 * Uses the existing Profile component with proper layout
 */
export default function ProfilePage() {
  return (
    <>
      <MainLayout>
        <div className="min-h-full bg-gray-50">
          <Profile />
        </div>
      </MainLayout>
      
      {/* Toast notifications */}
      <Toaster />
    </>
  );
}
