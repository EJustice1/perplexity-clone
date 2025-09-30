import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import TopicSubscriptionForm from "../TopicSubscriptionForm";

jest.mock("react-hot-toast", () => {
  return {
    __esModule: true,
    toast: {
      success: jest.fn(),
      error: jest.fn(),
      dismiss: jest.fn(),
    },
  };
});

const mockSubscribe = jest.fn().mockResolvedValue({
  subscription_id: "test-id",
  message: "Subscription saved.",
});

jest.mock("../../../services/api", () => ({
  apiService: {
    subscribeToTopic: (...args: unknown[]) => mockSubscribe(...args),
  },
}));

describe("TopicSubscriptionForm", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockSubscribe.mockClear();
    const { toast } = jest.requireMock("react-hot-toast");
    toast.success.mockClear();
    toast.error.mockClear();
    toast.dismiss.mockClear();
  });

  it("validates required fields before submission", async () => {
    render(<TopicSubscriptionForm />);

    fireEvent.submit(screen.getByRole("button", { name: /subscribe/i }).closest("form")!);

    expect(await screen.findByText(/enter a valid email address/i)).toBeInTheDocument();
  });

  it("submits form when inputs are valid and shows success message", async () => {
    render(<TopicSubscriptionForm />);

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "user@example.com" },
    });

    fireEvent.change(screen.getByLabelText(/topic of interest/i), {
      target: { value: "Artificial Intelligence" },
    });

    fireEvent.submit(screen.getByRole("button", { name: /subscribe/i }).closest("form")!);

    await waitFor(() => {
      expect(mockSubscribe).toHaveBeenCalledWith({
        email: "user@example.com",
        topic: "Artificial Intelligence",
      });
    });

    expect(screen.getByLabelText(/email address/i)).toHaveValue("");
    expect(screen.getByLabelText(/topic of interest/i)).toHaveValue("");
    const { toast } = jest.requireMock("react-hot-toast");
    expect(toast.success).toHaveBeenCalled();
  });

  it("populates topic input when suggestion is clicked", () => {
    render(<TopicSubscriptionForm />);

    fireEvent.click(screen.getByRole("button", { name: /artificial intelligence/i }));

    expect(screen.getByLabelText(/topic of interest/i)).toHaveValue("Artificial Intelligence");
  });

  it("shows error message when submission fails", async () => {
    mockSubscribe.mockRejectedValueOnce(new Error("Network Error"));

    render(<TopicSubscriptionForm />);

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "user@example.com" },
    });

    fireEvent.change(screen.getByLabelText(/topic of interest/i), {
      target: { value: "AI Research" },
    });

    fireEvent.submit(screen.getByRole("button", { name: /subscribe/i }).closest("form")!);

    expect(await screen.findByText(/network error/i)).toBeInTheDocument();
    const { toast } = jest.requireMock("react-hot-toast");
    expect(toast.error).toHaveBeenCalled();
  });
});


