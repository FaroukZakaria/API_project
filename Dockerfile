# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables for the Flask application
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project folder into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the Flask application
CMD ["flask", "run", "--port=8080", "--host=0.0.0.0"]