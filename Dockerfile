# Use Python slim image as base
FROM python:3.9-slim

# Install system dependencies required for LightGBM
RUN apt-get update && \
    apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port Flask will run on
EXPOSE 5000

# Run the application
CMD ["flask", "run"]
