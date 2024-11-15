# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and build script into the container
COPY requirements.txt /app/
COPY build.sh /app/

# Copy the current directory contents into the container at /app
COPY . /app

# Make the build script executable
RUN chmod +x /app/build.sh

# Run the build script
RUN /app/build.sh

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
