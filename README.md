# Flask Docker Demo

A simple Flask application that can be run locally using Docker. This application has been updated with the latest stable versions of Flask and Werkzeug, and includes comprehensive documentation with detailed docstrings for all functions and methods.

## Recent Updates

- **Library Updates**: Updated to Flask 3.0.3 and Werkzeug 3.0.4 for improved security and performance
- **Documentation**: Added comprehensive docstrings to all Python functions, methods, and classes following Python documentation standards
- **Code Quality**: Enhanced code documentation for better maintainability and developer experience

## Project Structure

```
.
├── app.py              # Main Flask application (with comprehensive docstrings)
├── test_app.py         # Unit tests (with comprehensive docstrings)
├── requirements.txt    # Python dependencies (updated versions)
├── validate_updates.py # Validation script for updates
├── Dockerfile          # Docker configuration
└── README.md           # This file
```

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine
- Python 3.9+ (for local development without Docker)

## Running the Application

### Using Docker

1. Build the Docker image:

```bash
docker build -t flask-docker-demo .
```

2. Run the container:

```bash
docker run -p 5000:5000 flask-docker-demo
```

3. Access the application at [http://localhost:5000](http://localhost:5000)

### Local Development (without Docker)

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

4. Access the application at [http://localhost:5000](http://localhost:5000)

## Validation and Testing

### Running the Validation Script

To validate that all updates are working correctly, run the validation script:

```bash
python validate_updates.py
```

This script will:
- Test that all libraries can be imported successfully
- Verify Flask application creation and route registration
- Validate that comprehensive docstrings are present
- Run the complete test suite to ensure functionality

### Running Unit Tests

To run the unit tests separately:

```bash
python -m unittest test_app.py -v
```

Or run individual tests:

```bash
python -m unittest test_app.FlaskAppTests.test_home_endpoint -v
python -m unittest test_app.FlaskAppTests.test_health_endpoint -v
```

## API Endpoints

- `GET /`: Returns a welcome message
- `GET /health`: Returns the health status of the application

## Development

To make changes to the application:

1. Modify the code as needed
2. If you add new dependencies, update `requirements.txt`
3. Rebuild the Docker image if using Docker

## License

This project is open-source and available under the MIT License.