FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=./src:./src/django_project/:$PYTHONPATH
ENV DJANGO_SETTINGS_MODULE=django_project.settings

# Install system packages using 'apk' (Alpine package manager)
# Used ChatGPT due to issues installing mysql
RUN apk update && \
    apk add --no-cache python3-dev libffi-dev gcc musl-dev mariadb-dev make && \
    apk add --no-cache --virtual .build-deps build-base && \
    pip install --no-cache-dir mysqlclient && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .
