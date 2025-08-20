#!/usr/bin/env python3
"""
Validation script for Flask Docker Demo Application updates.

This script validates that the library updates and docstring additions
are working correctly. It performs basic import tests and runs the
existing test suite to ensure compatibility.

Author: Flask Docker Demo Team
Version: 1.0.0
"""

import sys
import subprocess
import importlib.util


def test_imports():
    """
    Test that all required libraries can be imported successfully.
    
    Returns:
        bool: True if all imports succeed, False otherwise
    """
    print("Testing library imports...")
    
    try:
        import flask
        print(f"✓ Flask {flask.__version__} imported successfully")
        
        import werkzeug
        print(f"✓ Werkzeug {werkzeug.__version__} imported successfully")
        
        # Test that our app can be imported
        import app
        print("✓ Application module imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_app_creation():
    """
    Test that the Flask application can be created and configured.
    
    Returns:
        bool: True if app creation succeeds, False otherwise
    """
    print("\nTesting Flask application creation...")
    
    try:
        from app import app
        
        # Test that the app is a Flask instance
        from flask import Flask
        if isinstance(app, Flask):
            print("✓ Flask application instance created successfully")
        else:
            print("✗ Application is not a Flask instance")
            return False
            
        # Test that routes are registered
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        expected_routes = ['/', '/health']
        
        for route in expected_routes:
            if route in routes:
                print(f"✓ Route '{route}' registered successfully")
            else:
                print(f"✗ Route '{route}' not found")
                return False
                
        return True
        
    except Exception as e:
        print(f"✗ Application creation error: {e}")
        return False


def run_tests():
    """
    Run the existing test suite to ensure compatibility.
    
    Returns:
        bool: True if all tests pass, False otherwise
    """
    print("\nRunning test suite...")
    
    try:
        # Run the test suite
        result = subprocess.run([
            sys.executable, '-m', 'unittest', 'test_app.py', '-v'
        ], capture_output=True, text=True, cwd='/workspace')
        
        if result.returncode == 0:
            print("✓ All tests passed successfully")
            print("Test output:")
            print(result.stdout)
            return True
        else:
            print("✗ Some tests failed")
            print("Error output:")
            print(result.stderr)
            print("Standard output:")
            print(result.stdout)
            return False
            
    except Exception as e:
        print(f"✗ Error running tests: {e}")
        return False


def validate_docstrings():
    """
    Validate that docstrings have been added to all functions and classes.
    
    Returns:
        bool: True if docstrings are present, False otherwise
    """
    print("\nValidating docstrings...")
    
    try:
        import app
        import test_app
        
        # Check app.py docstrings
        if app.__doc__:
            print("✓ Module docstring present in app.py")
        else:
            print("✗ Module docstring missing in app.py")
            return False
            
        if app.home.__doc__:
            print("✓ Docstring present for home() function")
        else:
            print("✗ Docstring missing for home() function")
            return False
            
        if app.health.__doc__:
            print("✓ Docstring present for health() function")
        else:
            print("✗ Docstring missing for health() function")
            return False
            
        # Check test_app.py docstrings
        if test_app.__doc__:
            print("✓ Module docstring present in test_app.py")
        else:
            print("✗ Module docstring missing in test_app.py")
            return False
            
        if test_app.FlaskAppTests.__doc__:
            print("✓ Class docstring present for FlaskAppTests")
        else:
            print("✗ Class docstring missing for FlaskAppTests")
            return False
            
        # Check method docstrings
        methods_to_check = ['setUp', 'test_home_endpoint', 'test_health_endpoint']
        for method_name in methods_to_check:
            method = getattr(test_app.FlaskAppTests, method_name)
            if method.__doc__:
                print(f"✓ Docstring present for {method_name}() method")
            else:
                print(f"✗ Docstring missing for {method_name}() method")
                return False
                
        return True
        
    except Exception as e:
        print(f"✗ Error validating docstrings: {e}")
        return False


def main():
    """
    Main validation function that runs all validation tests.
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    print("Flask Docker Demo - Update Validation")
    print("=" * 40)
    
    all_passed = True
    
    # Run all validation tests
    tests = [
        ("Library Imports", test_imports),
        ("Application Creation", test_app_creation),
        ("Docstring Validation", validate_docstrings),
        ("Test Suite", run_tests),
    ]
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        
        if not test_func():
            all_passed = False
            
    print("\n" + "=" * 40)
    if all_passed:
        print("✓ All validation tests passed! Updates are successful.")
        return 0
    else:
        print("✗ Some validation tests failed. Please review the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())