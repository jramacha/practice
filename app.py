"""
Flask Docker Demo Application.

A simple Flask web application that provides basic endpoints for demonstration
purposes. This application is designed to run in a Docker container and provides
health check functionality.

Author: Flask Docker Demo Team
Version: 1.0.0
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    """
    Home endpoint that returns a welcome message.
    
    This endpoint serves as the main entry point for the application,
    providing a welcome message and success status to confirm the
    application is running correctly.
    
    Returns:
        flask.Response: JSON response containing welcome message and status.
            - message (str): Welcome message for the application
            - status (str): Success status indicator
            
    Example:
        GET / HTTP/1.1
        
        Response:
        {
            "message": "Welcome to the Flask Docker Demo",
            "status": "success"
        }
    """
    return jsonify({
        "message": "Welcome to the Flask Docker Demo",
        "status": "success"
    })


@app.route('/health')
def health():
    """
    Health check endpoint for monitoring application status.
    
    This endpoint provides a simple health check mechanism that can be used
    by monitoring systems, load balancers, or container orchestration
    platforms to verify that the application is running and responsive.
    
    Returns:
        flask.Response: JSON response containing health status.
            - status (str): Health status indicator ("healthy")
            
    Example:
        GET /health HTTP/1.1
        
        Response:
        {
            "status": "healthy"
        }
    """
    return jsonify({
        "status": "healthy"
    })

if __name__ == '__main__':
    # Run on all interfaces (0.0.0.0) to be accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)