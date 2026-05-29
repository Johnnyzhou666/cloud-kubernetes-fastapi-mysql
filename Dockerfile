# Use the official lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the dependencies file and install them
# Isolating this step leverages Docker's caching mechanism to accelerate subsequent builds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Expose port 80 for external access to the container
EXPOSE 80

# Run the Flask application
CMD ["python", "app.py"]
