# ollama-docker/Dockerfile

FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and install Ollama
# Replace the URL with the actual download link
RUN curl -Lo /usr/local/bin/ollama https://ollama.com/download/linux/ollama \
    && chmod +x /usr/local/bin/ollama

# Expose the default Ollama API port
EXPOSE 11434

# Start Ollama server
CMD ["ollama", "serve"]
