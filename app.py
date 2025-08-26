"""
Flask Docker Demo Application.

A simple Flask web application that provides basic endpoints for demonstration
purposes. This application is designed to run in a Docker container and provides
health check functionality.

Author: Flask Docker Demo Team
Version: 1.0.0
"""

from flask import Flask, jsonify
import sqlite3
from flask import g


app = Flask(__name__)

DATABASE = 'hits.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS hits (
            endpoint TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )''')
        for ep in ['/', '/health']:
            cursor.execute('INSERT OR IGNORE INTO hits (endpoint, count) VALUES (?, ?)', (ep, 0))
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



def increment_hit(endpoint):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE hits SET count = count + 1 WHERE endpoint = ?', (endpoint,))
    db.commit()

@app.route('/')
def home():
    increment_hit('/')
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
    increment_hit('/health')
    return jsonify({
        "status": "healthy"
    })

@app.route('/hits')
def hits():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT endpoint, count FROM hits')
    data = {row[0]: row[1] for row in cursor.fetchall()}
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    # Run on all interfaces (0.0.0.0) to be accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)