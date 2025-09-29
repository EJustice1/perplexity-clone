/**
 * Client component that captures email/topic subscriptions for Stage 1.
 */
"use client";

import React, { useState } from "react";
import { toast } from "react-hot-toast";
import { apiService } from "../../services/api";

/**
 * Topic subscription form for Stage 1 subscription capture requirements.
 * Presents email/topic inputs, validation, and submission feedback states.
 */
export default function TopicSubscriptionForm(): React.ReactElement {
  /**
   * Form field values for the subscription request.
   */
  const [formData, setFormData] = useState({ email: "", topic: "" });

  /**
   * Tracks the current submission lifecycle state for the form.
   */
  const [status, setStatus] = useState<
    "idle" | "submitting" | "success" | "error"
  >("idle");

  /**
   * Holds user-facing error messaging for validation or server issues.
   */
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const topicSuggestions = [
    "Artificial Intelligence",
    "Renewable Energy",
    "Financial Markets",
    "Healthcare Innovations",
    "Space Exploration",
    "Climate Policy",
  ];

  /**
   * Updates the specified form field and clears prior feedback messages.
   * @param field - Field key being updated.
   * @param value - New value entered by the user.
   */
  const handleInputChange = (field: "email" | "topic", value: string) => {
    setFormData((current) => ({ ...current, [field]: value }));
    setErrorMessage(null);
    toast.dismiss();
    if (status === "success") {
      setStatus("idle");
    }
  };

  /**
   * Applies a suggested topic to the topic field to streamline entry.
   * @param suggestion - Suggested topic string selected by the user.
   */
  const handleSuggestionClick = (suggestion: string) => {
    handleInputChange("topic", suggestion);
  };

  /**
   * Performs lightweight email format validation for the form.
   * @param value - Email address provided by the user.
   * @returns Boolean indicating whether the email appears valid.
   */
  const isValidEmail = (value: string): boolean => {
    const isValidFormat =
      /^(?:[a-zA-Z0-9_'^&/+-])+(?:\.(?:[a-zA-Z0-9_'^&/+-])+)*@(?:(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})$/u;
    return isValidFormat.test(value.trim().toLowerCase());
  };

  /**
   * Handles form submission, performs validation, and invokes the API call.
   * @param event - Form submission event.
   */
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage(null);
    toast.dismiss();

    if (!formData.email.trim() || !isValidEmail(formData.email)) {
      setErrorMessage("Enter a valid email address to subscribe.");
      setStatus("error");
      return;
    }

    if (!formData.topic.trim()) {
      setErrorMessage("Choose a topic to receive weekly updates.");
      setStatus("error");
      return;
    }

    try {
      setStatus("submitting");
      const response = await apiService.subscribeToTopic({
        email: formData.email.trim(),
        topic: formData.topic.trim(),
      });

      setStatus("success");
      toast.success(
        response.message ??
          "Subscription received. We will email weekly updates when available.",
      );
      setFormData({ email: "", topic: "" });
    } catch (error) {
      setStatus("error");
      const message =
        error instanceof Error
          ? error.message
          : "Unable to save your subscription. Try again later.";
      setErrorMessage(message);
      toast.error(message);
    }
  };

  return (
    <section className="bg-white dark:bg-gray-800 rounded-3xl shadow-lg border border-gray-200 dark:border-gray-700 px-6 py-8 sm:px-10">
      <div className="mx-auto max-w-2xl">
        <h1 className="text-3xl font-semibold text-gray-900 dark:text-white text-center">
          Weekly Topic Updates
        </h1>
        <p className="mt-3 text-center text-gray-600 dark:text-gray-300">
          Share your email and a topic you care about. We will send concise weekly recaps
          once new information is detected.
        </p>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit} noValidate>
          <div className="grid gap-6 sm:grid-cols-2">
            <div className="flex flex-col">
              <label
                htmlFor="subscription-email"
                className="text-sm font-medium text-gray-800 dark:text-gray-200"
              >
                Email address
              </label>
              <input
                id="subscription-email"
                type="email"
                required
                autoComplete="email"
                value={formData.email}
                onChange={(event) =>
                  handleInputChange("email", event.target.value)
                }
                className="mt-2 rounded-xl border border-gray-300 bg-transparent px-4 py-3 text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:border-gray-600 dark:text-gray-100 dark:focus:border-blue-400 dark:focus:ring-blue-500/40"
                placeholder="you@example.com"
                aria-describedby="subscription-email-help"
                aria-invalid={status === "error" && !!errorMessage}
              />
              <span
                id="subscription-email-help"
                className="mt-2 text-xs text-gray-500 dark:text-gray-400"
              >
                We only use this to deliver your weekly updates.
              </span>
            </div>

            <div className="flex flex-col">
              <label
                htmlFor="subscription-topic"
                className="text-sm font-medium text-gray-800 dark:text-gray-200"
              >
                Topic of interest
              </label>
              <input
                id="subscription-topic"
                type="text"
                required
                value={formData.topic}
                onChange={(event) =>
                  handleInputChange("topic", event.target.value)
                }
                className="mt-2 rounded-xl border border-gray-300 bg-transparent px-4 py-3 text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:border-gray-600 dark:text-gray-100 dark:focus:border-blue-400 dark:focus:ring-blue-500/40"
                placeholder="e.g. Generative AI"
                aria-describedby="subscription-topic-help"
                aria-invalid={status === "error" && !!errorMessage}
              />
              <span
                id="subscription-topic-help"
                className="mt-2 text-xs text-gray-500 dark:text-gray-400"
              >
                Pick anything—companies, technologies, industries, or policies.
              </span>
            </div>
          </div>

          <div>
            <p className="text-sm font-medium text-gray-800 dark:text-gray-200">
              Popular this week
            </p>
            <div className="mt-3 flex flex-wrap gap-2">
              {topicSuggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="rounded-full border border-blue-200 px-4 py-2 text-sm text-blue-700 transition hover:border-blue-400 hover:bg-blue-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-400 dark:border-blue-400/60 dark:text-blue-200 dark:hover:border-blue-300 dark:hover:bg-blue-500/30"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>

          {errorMessage ? (
            <div
              role="alert"
              className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-500/40 dark:bg-red-500/10 dark:text-red-200"
            >
              {errorMessage}
            </div>
          ) : null}

          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <p className="text-xs text-gray-500 dark:text-gray-400">
              By subscribing you agree to receive weekly email summaries for this topic.
            </p>
            <button
              type="submit"
              disabled={status === "submitting"}
              className="inline-flex items-center justify-center rounded-full bg-blue-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-400 disabled:cursor-not-allowed disabled:bg-blue-400 dark:bg-blue-500 dark:hover:bg-blue-400"
            >
              {status === "submitting" ? "Submitting…" : "Subscribe"}
            </button>
          </div>
        </form>
      </div>
    </section>
  );
}


