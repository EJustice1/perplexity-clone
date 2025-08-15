import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Get the backend service URL from environment variables
    // In development, use localhost; in production, use the Cloud Run service URL
    const backendUrl = process.env.NODE_ENV === 'development' 
      ? 'http://localhost:8000'
      : process.env.BACKEND_SERVICE_URL;
    
    if (!backendUrl) {
      console.error('BACKEND_SERVICE_URL environment variable is not set in production');
      return NextResponse.json(
        { error: 'Backend service not configured' },
        { status: 500 }
      );
    }

    console.log(`Proxying request to backend: ${backendUrl}/api/v1/process-text`);
    console.log(`Environment: ${process.env.NODE_ENV}`);
    console.log(`BACKEND_SERVICE_URL: ${process.env.BACKEND_SERVICE_URL}`);

    // Get the request body
    const requestBody = await request.json();
    console.log(`Request body:`, requestBody);

    // Forward the request to the backend service
    const backendResponse = await fetch(`${backendUrl}/api/v1/process-text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Forward any relevant headers
        ...(request.headers.get('authorization') && {
          'authorization': request.headers.get('authorization')!
        }),
      },
      body: JSON.stringify(requestBody),
    });

    console.log(`Backend response status: ${backendResponse.status}`);
    console.log(`Backend response headers:`, Object.fromEntries(backendResponse.headers.entries()));

    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      console.error(`Backend returned error: ${backendResponse.status} - ${errorText}`);
      return NextResponse.json(
        { error: `Backend error: ${errorText}` },
        { status: backendResponse.status }
      );
    }

    // Get the response data
    const responseData = await backendResponse.json();
    console.log(`Backend response data:`, responseData);

    // Return the response with the same status code
    return NextResponse.json(responseData, { status: backendResponse.status });

  } catch (error) {
    console.error('Error proxying request to backend:', error);
    return NextResponse.json(
      { error: 'Failed to communicate with backend service', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

// Handle OPTIONS request for CORS preflight
export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
