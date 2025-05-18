# Use the official Python base image
FROM python:3.12

# Disable .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire Django project
COPY . .

# Run Django using Gunicorn for production
CMD ["gunicorn", "log_dashboard.wsgi:application", "--bind", "0.0.0.0:8000"]
