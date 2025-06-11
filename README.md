# Flask Docker Demo

A simple Flask application that can be run locally using Docker.

## Project Structure

```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── .dockerignore       # Files to exclude from Docker build
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