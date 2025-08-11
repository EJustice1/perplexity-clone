from flask import Flask, render_template_string, request, Response
from src.middleware import (
    create_flask_middleware,
    get_metrics_response,
    get_health_response
)
from src.core.config import frontend_config

app = Flask(__name__)

# Configure Flask with centralized settings
app.config['SECRET_KEY'] = frontend_config.SECRET_KEY
app.config['TEMPLATES_AUTO_RELOAD'] = frontend_config.TEMPLATES_AUTO_RELOAD

# Create metrics middleware instance (fully functional)
metrics_middleware = create_flask_middleware(frontend_config.SERVICE_NAME)

# Note: Auth, caching, and rate limiting middleware are skeletons and disabled by default
# They can be enabled and implemented later when needed

@app.before_request
def before_request():
    """Standardized before_request handler."""
    metrics_middleware.before_request(request)

@app.after_request
def after_request(response):
    """Standardized after_request handler."""
    response = metrics_middleware.after_request(request, response)
    return response

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Perplexity Clone</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
                h1 { color: #333; }
            </style>
        </head>
        <body>
            <h1>Perplexity Clone</h1>
            <p>Welcome to the frontend!</p>
        </body>
        </html>
    ''')

@app.route('/metrics')
def metrics():
    """Standardized metrics endpoint."""
    content, media_type = get_metrics_response()
    return Response(content, mimetype=media_type)

@app.route('/health')
def health():
    """Standardized health endpoint."""
    return get_health_response(frontend_config.SERVICE_NAME)

# TODO: Add these endpoints when middleware is fully implemented
# @app.route('/protected')
# def protected_page():
#     """Protected page requiring authentication."""
#     return render_template_string('''
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <title>Protected Page</title>
#             <style>
#                 body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
#                 h1 { color: #333; }
#             </style>
#         </head>
#         <body>
#             <h1>Protected Page</h1>
#             <p>This is a protected page that requires authentication.</p>
#         </body>
#         </html>
#     ''')

# @app.route('/cache-test')
# def cache_test():
#     """Test endpoint for caching."""
#     import time
#     return {
#         "message": "Cached response from frontend",
#         "timestamp": time.time(),
#         "service": frontend_config.SERVICE_NAME
#     }

if __name__ == '__main__':
    app.run(
        debug=frontend_config.DEBUG,
        host=frontend_config.FRONTEND_HOST,
        port=frontend_config.FRONTEND_PORT
    )
