# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set environment variables to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and other necessary packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip bash && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Ensure entrypoint.sh is executable
RUN chmod +x /app/entrypoint.sh

# Set the default entrypoint
CMD ["/bin/bash", "/app/entrypoint.sh"]
