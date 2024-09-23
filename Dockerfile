FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .



# Set the PYTHONPATH to /app to ensure Python can find the 'bot' package
ENV PYTHONPATH=/app

# Expose port for health checks
EXPOSE 8080

# Command to run the bot using module execution
CMD ["python", "-m", "bot.main"]
