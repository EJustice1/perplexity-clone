"use client";

import { Toaster } from "react-hot-toast";
import MainLayout from "../../components/layout/MainLayout";
import { SubscribedTopics } from "../../components/features";

/**
 * Topics page - Placeholder for subscribed topics management
 * Reuses the new SubscribedTopics component for consistent styling
 * Client component to support theme switching and future interactive features
 */
export default function TopicsPage() {
  return (
    <>
      <MainLayout>
        <div className="min-h-full bg-gray-50 dark:bg-gray-900">
          <SubscribedTopics />
        </div>
      </MainLayout>

      {/* Toast notifications */}
      <Toaster />
    </>
  );
}

