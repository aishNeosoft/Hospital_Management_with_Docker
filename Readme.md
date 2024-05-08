# Hospital Management System

## Description

This project is a web application for a hospital management system where users can interact based on their roles. The system supports the following roles:

- **Admin**: Manages overall system settings and user roles.
- **Hospital**: Manages hospital-related information and settings.
- **Doctor**: Adds and views medical records for patients.
- **Patient**: Views personal medical reports and information.

### Features

- **User Roles**: Different users have specific roles and permissions within the system.
- **Medical Records**: Doctors can add medical records (e.g., body temperature) for patients.
- **Chart Visualization**: Patients can view their medical reports in chart format.
- **Web Interface**: Provides a user-friendly web interface for interacting with the hospital management system.

## Running the Project

### Using Docker

To run this project using Docker, follow these steps:

1. **Build Docker Image**:
   ```bash
   docker-compose build web

2. Run the project on "0.0.0.0:8000" server:
   docker-compose up

## Running the Project on Django Server

1. Make virtualenv venv and activate it
2. Check proper project directory
3. install all the dependencies from requirements.txt:
   - pip install -r requirements.txt
4. Create the migrations for database:
   - python manage.py makemigrations
   - python manage.py migrate
5. Run The server:
   - python manage.py runserver
6. Make Your First signup with signUp page
