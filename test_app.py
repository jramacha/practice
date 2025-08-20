"""
Unit tests for Flask Docker Demo Application.

This module contains comprehensive unit tests for the Flask application endpoints,
ensuring that all routes return the expected responses and status codes.
The tests use Flask's built-in test client for making HTTP requests.

Test Coverage:
    - Home endpoint (/) functionality and response format
    - Health check endpoint (/health) functionality and response format

Author: Flask Docker Demo Team
Version: 1.0.0
"""

import unittest
import json
from app import app


class FlaskAppTests(unittest.TestCase):
    """
    Test suite for Flask Docker Demo Application.
    
    This class contains unit tests that verify the correct behavior of all
    application endpoints. It uses Flask's test client to simulate HTTP
    requests and validates both response status codes and JSON content.
    
    Attributes:
        app: Flask test client instance for making HTTP requests
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        
        This method is called before each individual test method to prepare
        the test environment. It creates a Flask test client and enables
        testing mode for better error reporting during tests.
        
        Note:
            This method is automatically called by the unittest framework
            before each test method execution.
        """
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_endpoint(self):
        """
        Test the home endpoint (/) for correct response and content.
        
        This test verifies that the home endpoint returns a 200 status code
        and the expected JSON response containing a welcome message and
        success status. It validates both the structure and content of
        the response.
        
        Assertions:
            - Response status code is 200 (OK)
            - Response contains correct welcome message
            - Response contains success status
            
        Raises:
            AssertionError: If any of the expected response conditions are not met
        """
        response = self.app.get('/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Welcome to the Flask Docker Demo')
        self.assertEqual(data['status'], 'success')
    
    def test_health_endpoint(self):
        """
        Test the health check endpoint (/health) for correct response.
        
        This test verifies that the health endpoint returns a 200 status code
        and the expected JSON response indicating the application is healthy.
        This endpoint is typically used by monitoring systems and load balancers.
        
        Assertions:
            - Response status code is 200 (OK)
            - Response contains healthy status indicator
            
        Raises:
            AssertionError: If any of the expected response conditions are not met
        """
        response = self.app.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')

if __name__ == '__main__':
    unittest.main()