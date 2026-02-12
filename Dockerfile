# Start from official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency files first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY run.sh .
COPY ./app ./app
COPY ./pipelines ./pipelines

# Expose port
EXPOSE 8000 3000

# Start server
CMD ["./run.sh"]