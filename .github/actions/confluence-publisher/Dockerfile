# Use the official Python 3.9-slim base image for reproducibility
FROM python:3.9.18-slim

# Set working directory
WORKDIR /app

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
# Copy all application source files into the container
COPY . .
# Copy the rest of the application code
COPY entrypoint.py .

# Set the default command for the container
CMD ["python3", "entrypoint.py"]