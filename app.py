"""
Flask Docker Demo Application.

A simple Flask web application that provides basic endpoints for demonstration
purposes. This application is designed to run in a Docker container and provides
health check functionality with hit counter tracking.

Author: Flask Docker Demo Team
Version: 1.0.0
"""

import sqlite3
import threading
from flask import Flask, jsonify

app = Flask(__name__)

# Database configuration
DATABASE_PATH = 'hits.db'
db_lock = threading.Lock()


def init_database():
    """
    Initialize the SQLite database and create the hits table if it doesn't exist.
    
    This function sets up the database schema for tracking endpoint hits.
    The hits table stores the endpoint path and the number of hits for each endpoint.
    
    Table Schema:
        - endpoint (TEXT PRIMARY KEY): The endpoint path (e.g., '/', '/health')
        - hits (INTEGER): The number of hits for that endpoint
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hits (
                endpoint TEXT PRIMARY KEY,
                hits INTEGER DEFAULT 0
            )
        ''')
        conn.commit()


def increment_hit_count(endpoint):
    """
    Increment the hit count for a specific endpoint.
    
    This function uses an UPSERT operation (INSERT OR REPLACE) to either
    create a new record for the endpoint or increment the existing hit count.
    Thread-safe operation using a database lock.
    
    Args:
        endpoint (str): The endpoint path to increment hits for
        
    Returns:
        bool: True if the operation was successful, False otherwise
    """
    try:
        with db_lock:
            with sqlite3.connect(DATABASE_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO hits (endpoint, hits)
                    VALUES (?, COALESCE((SELECT hits FROM hits WHERE endpoint = ?), 0) + 1)
                ''', (endpoint, endpoint))
                conn.commit()
        return True
    except sqlite3.Error:
        # Gracefully handle database errors without affecting endpoint functionality
        return False


def get_hit_counts():
    """
    Retrieve all hit counts from the database.
    
    Returns:
        dict: A dictionary mapping endpoint paths to their hit counts.
              Returns empty dict if database operation fails.
    """
    try:
        with db_lock:
            with sqlite3.connect(DATABASE_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT endpoint, hits FROM hits ORDER BY endpoint')
                results = cursor.fetchall()
                return {endpoint: hits for endpoint, hits in results}
    except sqlite3.Error:
        return {}


# Initialize database when the module is loaded
init_database()


@app.route('/')
def home():
    """
    Home endpoint that returns a welcome message.
    
    This endpoint serves as the main entry point for the application,
    providing a welcome message and success status to confirm the
    application is running correctly. Hit count is tracked for this endpoint.
    
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
    # Track hit for this endpoint
    increment_hit_count('/')
    
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
    Hit count is tracked for this endpoint.
    
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
    # Track hit for this endpoint
    increment_hit_count('/health')
    
    return jsonify({
        "status": "healthy"
    })


@app.route('/hits')
def hits():
    """
    Hit counter endpoint that returns the current hit counts for all tracked endpoints.
    
    This endpoint provides visibility into how many times each tracked endpoint
    has been accessed. It retrieves the hit counts from the SQLite database
    and returns them in a structured JSON format.
    
    Returns:
        flask.Response: JSON response containing hit counts for all endpoints.
            - hits (dict): Dictionary mapping endpoint paths to their hit counts
            - total_hits (int): Total number of hits across all endpoints
            
    Example:
        GET /hits HTTP/1.1
        
        Response:
        {
            "hits": {
                "/": 5,
                "/health": 3
            },
            "total_hits": 8
        }
    """
    hit_counts = get_hit_counts()
    total_hits = sum(hit_counts.values()) if hit_counts else 0
    
    return jsonify({
        "hits": hit_counts,
        "total_hits": total_hits
    })

if __name__ == '__main__':
    # Run on all interfaces (0.0.0.0) to be accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)