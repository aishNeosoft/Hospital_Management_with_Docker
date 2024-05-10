# Hospital Management System

## Description

This project is a web application for a hospital management system where users can interact based on their roles. The system supports the following roles:

- **Admin**: Manages overall system settings and user roles.
- **Doctor**: Adds and views medical records for patients.
- **Patient**: Views personal medical reports and information.

### Features

- **User Roles**: Different users have specific roles and permissions within the system.
- **Medical Records**: Doctors can add medical records (e.g., body temperature) for patients.
- **Chart Visualization**: Patients can view their medical reports in line chart format.
- **Web Interface**: Provides a user-friendly web interface for interacting with the hospital management system.

## Running the Project

### Using Docker

To run this project using Docker, follow these steps:

1. **Build Docker Image**:
   ```bash
   docker-compose build web

2. Run the project on "0.0.0.0:8000" server:
   ```bash
   docker-compose up

## Running the Project on Django Server

1. Make virtualenv venv and activate it
   ```bash
   virtualenv venv

2. Check proper project directory

3. install all the dependencies from requirements.txt:
   ```bash
   pip install -r requirements.txt

4. Create the migrations for database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. Run The server:
   ```bash
   python manage.py runserver

6. Make Your First signup with signUp page

# Set up your Database Configuration with .env file

1. Add all the configuration into .env file create your database and add into DB_DATABASE key
   ```bash
   DB_CONNECTION=mysql
   DB_HOST= 'Your Host name' (default : 127.0.0.1)
   DB_PORT= 'Your DB PORT'
   DB_DATABASE= 'Your DB Name'
   DB_USERNAME= 'Your DB Username'
   DB_PASSWORD='Your DB Password'