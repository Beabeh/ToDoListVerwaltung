# Dockerfile
FROM python:3.8-alpine

# Install Flask
RUN pip install flask

# Set working directory in container
WORKDIR /app

# Copy your Python script into the container
COPY webapp.py /app

# Define how to run the app
ENTRYPOINT ["python"]
CMD ["webapp.py"]
