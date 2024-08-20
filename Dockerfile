# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app/

# Set environment variables
ENV FLASK_ENV=development
ENV FLASK_APP=app.py

# Expose port 5500 to the outside world
EXPOSE 5500

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5500"]
