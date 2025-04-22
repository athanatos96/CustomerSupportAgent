FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    ffmpeg \
    alsa-utils \
    pulseaudio \
    && apt-get clean

RUN apt update
RUN apt install build-essential -y

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command (you can override with CLI)
CMD ["python", "main.py"]
