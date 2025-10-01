"""
Main FastAPI application entry point.
"""

import logging
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from .middleware import LoggingMiddleware, TimeoutMiddleware
from .core.app_settings import app_settings
from .api import api_router
from .services.firestore_subscription_service import FirestoreSubscriptionService
from .services.dispatcher_service import DispatcherService
from .services.email_sender import EmailSender
from .services.email_dispatcher import EmailDispatcher

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(
    f"Starting {app_settings.app_name} v{app_settings.app_version}"
)
logger.info(f"Environment: {app_settings.environment}")
logger.info(f"Host: {app_settings.host}:{app_settings.port}")

app = FastAPI(
    title=app_settings.app_name,
    description=app_settings.app_description,
    version=app_settings.app_version,
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Global exception handler to catch any unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    logger.error(f"Request URL: {request.url}")
    logger.error(f"Request method: {request.method}")
    logger.error(f"Request headers: {dict(request.headers)}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc),
            "type": type(exc).__name__,
        },
    )


# Enhanced CORS middleware configuration
logger.info(
    f"Configuring CORS with origins: {app_settings.get_cors_origins()}"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["Content-Length", "Content-Type"],
    max_age=86400,  # Cache preflight response for 24 hours
)

logger.info("Adding LoggingMiddleware")
app.add_middleware(LoggingMiddleware)

logger.info("Adding TimeoutMiddleware")
app.add_middleware(TimeoutMiddleware, timeout_seconds=120)

logger.info("Including API router")
app.include_router(api_router)


@app.post("/dispatcher/dispatch")
async def dispatcher_dispatch() -> Response:
    """Accept weekly Cloud Scheduler trigger and return immediately."""

    logger.info("Dispatcher trigger received at /dispatcher/dispatch")
    firestore_service = FirestoreSubscriptionService(
        project_id=app_settings.gcp_project_id,
        collection_name=app_settings.firestore_collection,
    )
    dispatcher_service = DispatcherService(firestore_service)
    batches = dispatcher_service.gather_batches()

    email_sender = EmailSender(
        host=app_settings.smtp_host,
        port=app_settings.smtp_port,
        username=app_settings.smtp_username,
        password=app_settings.smtp_password,
        use_tls=app_settings.smtp_use_tls,
    )
    email_dispatcher = EmailDispatcher(
        email_sender=email_sender,
        firestore_service=firestore_service,
        sender_email=app_settings.smtp_from,
    )
    batch_counts = email_dispatcher.dispatch(
        {batch.topic: batch.emails for batch in batches}
    )
    logger.info("Emails dispatched per topic: %s", batch_counts)
    return Response(status_code=204)

logger.info("Application startup complete")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=app_settings.host, port=app_settings.port)
