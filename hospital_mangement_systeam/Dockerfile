# Use an official Python runtime as a base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt || { echo "Failed to install requirements"; exit 1; }

# Copy the project files into the container
COPY . .

# Copy entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Set executable permissions for entrypoint script
RUN chmod +x /app/entrypoint.sh

# Apply migrations and start Django development server using entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]