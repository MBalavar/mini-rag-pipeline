# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install NumPy first to avoid binary incompatibility issues
RUN python -m pip install --no-cache-dir "numpy>=1.22.4,<2.3.0"

# Copy requirements.txt
COPY requirements.txt .

# Install other Python dependencies
RUN python -m pip install --no-cache-dir -r requirements.txt



# Copy project files
COPY . .

# Create a non-root user
RUN useradd -m myuser
USER myuser

# Define default command
CMD ["python", "test.py"]