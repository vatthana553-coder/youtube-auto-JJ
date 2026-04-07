# Faceless Viral Video Bot - Public Deployment Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (FFmpeg, fonts, image libraries)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    wget \
    git \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7 \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p projects output logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FFMPEG_BINARY=ffmpeg

# Default command: Run the demo generator
CMD ["python", "src/main.py", "--demo"]
