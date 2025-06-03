# Use the official Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client
# Copy the application code
COPY . .

# Expose the port the app will run on
EXPOSE 8000

#