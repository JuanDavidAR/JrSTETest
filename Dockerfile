# Build stage
FROM python:3.11-alpine AS builder

# Install necessary build dependencies and MySQL client
RUN apk add --no-cache \
        build-base \
        mariadb-connector-c-dev

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt files
COPY requirements.txt .

# Install dependencies in an isolated environment
RUN pip install --upgrade pip==23.2.1 setuptools==70.0.0 wheel \
        && pip install --user -r requirements.txt

# Final stage
FROM python:3.11-alpine

# Copy installed dependencies from the previous stage
COPY --from=builder /root/.local /root/.local

# Add Python package directory to PATH
ENV PATH=/root/.local/bin:$PATH

# Install necessary MySQL client dependencies
RUN apk add --no-cache \
        mariadb-connector-c

# Set the working directory to /app
WORKDIR /app

# Copy all files from the current directory to the container at /app
COPY . .

# Expose port 8080 to allow access to the Flask application
EXPOSE 8080

# Command to run the application when the container starts
CMD ["python", "app.py"]
