# Backend Project

## Overview
This is a backend service built with **FastAPI** for task management, integrating AI-based scheduling and reminders.

## Features
- Task scheduling and AI-based task prioritization
- User authentication (OAuth, JWT)
- Role-based access control
- RESTful API endpoints
- Services for extended functionality
- Dockerized deployment

## Installation & Setup
### Prerequisites
- Python 3.8+
- Docker (optional)
- MongoDB (or another DB as configured)

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the API
```bash
uvicorn app.main:app --reload
```

## Docker Setup
To build and run the service in Docker:
```bash
docker build -t backend-app .
docker run -p 8000:8000 backend-app
```

## Project Structure
```
backend/
│── app/
│   │── core/         # Core logic & settings
│   │── models/       # Database models
│   │── routes/       # API endpoints
│   │── services/     # Business logic and additional services
│   │── ai/           # AI-based scheduling
│   │── main.py       # Main FastAPI application
│── tests/            # Unit tests
│── requirements.txt  # Dependencies
│── Dockerfile        # Docker setup
│── .env              # Environment variables
```

## API Endpoints
For API documentation, run the server and visit:
```
http://127.0.0.1:8000/docs
```

## Testing
Run tests using:
```bash
pytest tests/
```

## Contributing
1. Fork the repo
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a pull request

## License
MIT License
