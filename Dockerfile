# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY backend/requirements.txt /app/

# Install any dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the backend code into the container
COPY backend /app/

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the Django development server
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]

