import { NextRequest, NextResponse } from "next/server";

const SUBSCRIPTIONS_ENDPOINT = "/api/v1/subscriptions";

function resolveBackendUrl(): string {
  if (process.env.NODE_ENV === "production") {
    if (process.env.BACKEND_SERVICE_URL) {
      return process.env.BACKEND_SERVICE_URL;
    }
    return "http://backend:8000";
  }

  return "http://localhost:8000";
}

export async function POST(request: NextRequest) {
  try {
    const backendUrl = resolveBackendUrl();
    const body = await request.json();

    const response = await fetch(`${backendUrl}${SUBSCRIPTIONS_ENDPOINT}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    const payload = await response.json().catch(() => null);

    if (!response.ok) {
      return NextResponse.json(
        {
          error: "Subscription failed",
          detail: payload?.detail ?? response.statusText,
        },
        { status: response.status },
      );
    }

    return NextResponse.json(payload, { status: response.status });
  } catch (error) {
    return NextResponse.json(
      {
        error: "Failed to communicate with backend service",
        detail: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 },
    );
  }
}

export async function OPTIONS() {
  return NextResponse.json(null, {
    status: 200,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization",
    },
  });
}


