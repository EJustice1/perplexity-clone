"use client";

import { Toaster } from "react-hot-toast";
import MainLayout from "../../components/layout/MainLayout";
import {
  TopicSubscriptionForm,
  TopicSubscriptionHighlights,
} from "../../components/features";

/**
 * Topics page - Hosts Stage 1 topic subscription capture UI
 * Provides future-friendly layout for subscription management enhancements
 * Client component to support theme switching and interactive form states
 */
export default function TopicsPage() {
  return (
    <>
      <MainLayout>
        <div className="min-h-full bg-gray-50 dark:bg-gray-900">
          <div className="px-4 py-10 sm:px-8">
            <div className="mx-auto flex max-w-5xl flex-col gap-10">
              <TopicSubscriptionForm />
              <TopicSubscriptionHighlights />
            </div>
          </div>
        </div>
      </MainLayout>

      {/* Toast notifications */}
      <Toaster />
    </>
  );
}

