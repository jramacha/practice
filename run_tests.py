#!/usr/bin/env python3
"""
Test runner script for the Flask application.
"""

import subprocess
import sys
import os

def run_tests():
    """Run the unit tests for the Flask application."""
    try:
        # Change to the workspace directory
        os.chdir('/workspace')
        
        # Run the tests
        result = subprocess.run([
            sys.executable, '-m', 'unittest', 'test_app.py', '-v'
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        print(f"\nReturn code: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)