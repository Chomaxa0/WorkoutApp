# WorkoutApp API

## Introduction
Fitness API is a RESTful web service built with Django that allows users to create and track personalized workout plans. The API provides functionality for authentication, exercise selection, workout customization, calorie goal tracking, and real-time workout execution.

## Features
- User authentication with JWT Token (register, login, logout)
- Predefined exercise database with detailed information
- Customizable workout plans consisting of exercises that have sets, reps, duration as properties
- Workout progress tracking, including burned calories
- Weekly workout planning with adjustable frequency for specific workouts
- Calorie goal tracking with estimated time to goal completion in weeks
- Real-time workout execution via API endpoint interactions
- API documentation using Swagger
- Fully containerized with Docker

## Installation, Configuration, Deployment
### Prerequisites
- Docker & Docker Compose installed on the system
To deploy the API using Docker, follow these steps:

### Steps to deploy the API using Docker, follow these steps:
1. Clone the repository:
   ```sh
   git clone https://github.com/Chomaxa0/WorkoutApp.git
   ```
2. Run the project from the project directory using cmd command:
   ```sh
   docker compose up
   ```
3. The API will be available at:
   ```sh
   http://localhost:8000/ and/or http://localhost:8000/swagger
   ```

## API Documentation
The API provides documentation using Swagger. Once the server is running, you can access the documentation at:
- `http://127.0.0.1:8000/swagger/`

## Database and Seeding
- Uses SQLite3 as the default database
- An automatic seed script is provided to populate the exercise database:

## Authentication
The API uses JWT for authentication. Users must first obtain a token to access protected endpoints.
- Obtain access token: `POST /user/register/`
- Refresh token: `POST /user/refresh/`

## Error Handling
The API returns appropriate status codes and messages for errors.
| Status Code | Meaning |
|-------------|---------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |
