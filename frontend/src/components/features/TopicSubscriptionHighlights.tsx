/**
 * Client component that showcases subscription benefits on the topics page.
 */
"use client";

import React from "react";

interface HighlightItem {
  /**
   * Title summarizing the highlight.
   */
  title: string;
  /**
   * Supporting copy providing additional context.
   */
  description: string;
}

const highlightItems: HighlightItem[] = [
  {
    title: "Curated weekly refresh",
    description:
      "Receive one concise email every Monday morning covering the developments that matter most for your topic.",
  },
  {
    title: "Noise-free updates",
    description:
      "Our future change detection pipeline flags only new sources and insights so you avoid redundant recaps.",
  },
  {
    title: "Simple controls",
    description:
      "Update or pause subscriptions anytime once the management dashboard launches in the next stage.",
  },
];

/**
 * Renders a highlight section that explains the value of subscribing.
 * Provides supporting information adjacent to the primary subscription form.
 */
export default function TopicSubscriptionHighlights(): React.ReactElement {
  return (
    <section className="rounded-3xl border border-gray-200 bg-white px-6 py-8 shadow-sm dark:border-gray-700 dark:bg-gray-800 sm:px-10">
      <div className="mx-auto max-w-3xl">
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
          Why subscribe now?
        </h2>
        <p className="mt-2 text-gray-600 dark:text-gray-300">
          We are building a lean weekly digest that focuses on surfacing meaningful changes. Here is what to expect as Stage 1 rolls out.
        </p>

        <dl className="mt-6 grid gap-6 md:grid-cols-3">
          {highlightItems.map((item) => (
            <div
              key={item.title}
              className="rounded-2xl border border-blue-100 bg-blue-50/60 p-4 text-blue-900 transition hover:border-blue-200 hover:bg-blue-50 dark:border-blue-500/30 dark:bg-blue-500/10 dark:text-blue-100"
            >
              <dt className="text-sm font-medium uppercase tracking-wide">
                {item.title}
              </dt>
              <dd className="mt-2 text-sm text-blue-800 dark:text-blue-200">
                {item.description}
              </dd>
            </div>
          ))}
        </dl>
      </div>
    </section>
  );
}


