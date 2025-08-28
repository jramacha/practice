"""
Unit tests for Flask Docker Demo Application.

This module contains comprehensive unit tests for the Flask application endpoints,
ensuring that all routes return the expected responses and status codes.
The tests use Flask's built-in test client for making HTTP requests and include
testing for the hit counter functionality.

Test Coverage:
    - Home endpoint (/) functionality and response format
    - Health check endpoint (/health) functionality and response format
    - Hit counter endpoint (/hits) functionality and hit tracking

Author: Flask Docker Demo Team
Version: 1.0.0
"""

import unittest
import json
import os
import sqlite3
from app import app, DATABASE_PATH, init_database


class FlaskAppTests(unittest.TestCase):
    """
    Test suite for Flask Docker Demo Application.
    
    This class contains unit tests that verify the correct behavior of all
    application endpoints. It uses Flask's test client to simulate HTTP
    requests and validates both response status codes and JSON content.
    Includes comprehensive testing of the hit counter functionality.
    
    Attributes:
        app: Flask test client instance for making HTTP requests
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        
        This method is called before each individual test method to prepare
        the test environment. It creates a Flask test client, enables
        testing mode, and sets up a clean database state for testing.
        
        Note:
            This method is automatically called by the unittest framework
            before each test method execution.
        """
        self.app = app.test_client()
        self.app.testing = True
        
        # Clean up any existing test database
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
        
        # Initialize a fresh database for testing
        init_database()
    
    def tearDown(self):
        """
        Clean up test fixtures after each test method.
        
        This method removes the test database file to ensure a clean
        state for subsequent tests.
        """
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
    
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
    
    def test_hits_endpoint_initial_state(self):
        """
        Test the hits endpoint (/hits) returns correct initial state.
        
        This test verifies that the hits endpoint returns a 200 status code
        and shows zero hits initially when no endpoints have been accessed.
        
        Assertions:
            - Response status code is 200 (OK)
            - Response contains empty hits dictionary
            - Total hits is 0
            
        Raises:
            AssertionError: If any of the expected response conditions are not met
        """
        response = self.app.get('/hits')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['hits'], {})
        self.assertEqual(data['total_hits'], 0)
    
    def test_hit_counter_functionality(self):
        """
        Test that hit counters are properly incremented for tracked endpoints.
        
        This test verifies that accessing the home and health endpoints
        properly increments their respective hit counters and that the
        hits endpoint accurately reports these counts.
        
        Assertions:
            - Hit counts are properly tracked for each endpoint
            - Total hits calculation is correct
            - Multiple hits to same endpoint increment correctly
            
        Raises:
            AssertionError: If hit counting is not working correctly
        """
        # Access home endpoint twice
        self.app.get('/')
        self.app.get('/')
        
        # Access health endpoint once
        self.app.get('/health')
        
        # Check hit counts
        response = self.app.get('/hits')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['hits']['/'], 2)
        self.assertEqual(data['hits']['/health'], 1)
        self.assertEqual(data['total_hits'], 3)
    
    def test_hits_endpoint_not_counted(self):
        """
        Test that accessing the /hits endpoint itself is not counted.
        
        This test verifies that the /hits endpoint does not track its own
        hits, which would create unnecessary noise in the hit counter data.
        
        Assertions:
            - /hits endpoint is not included in hit counts
            - Accessing /hits multiple times doesn't affect other counts
            
        Raises:
            AssertionError: If /hits endpoint is incorrectly being tracked
        """
        # Access hits endpoint multiple times
        self.app.get('/hits')
        self.app.get('/hits')
        self.app.get('/hits')
        
        # Check that hits endpoint is not tracked
        response = self.app.get('/hits')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['hits'], {})
        self.assertEqual(data['total_hits'], 0)
    
    def test_mixed_endpoint_access_pattern(self):
        """
        Test hit counting with a mixed pattern of endpoint access.
        
        This test simulates a realistic usage pattern with multiple
        accesses to different endpoints in various orders to ensure
        the hit counter works correctly in all scenarios.
        
        Assertions:
            - All endpoint hits are correctly counted
            - Order of access doesn't affect counting accuracy
            - Total hits calculation remains accurate
            
        Raises:
            AssertionError: If hit counting fails with mixed access patterns
        """
        # Mixed access pattern
        self.app.get('/')           # home: 1
        self.app.get('/health')     # health: 1
        self.app.get('/')           # home: 2
        self.app.get('/hits')       # not counted
        self.app.get('/health')     # health: 2
        self.app.get('/')           # home: 3
        
        # Verify final counts
        response = self.app.get('/hits')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['hits']['/'], 3)
        self.assertEqual(data['hits']['/health'], 2)
        self.assertEqual(data['total_hits'], 5)


if __name__ == '__main__':
    unittest.main()