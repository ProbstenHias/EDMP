# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5002 available to the world outside this container
EXPOSE 5002

VOLUME /app/dags


# Run app.py when the container launches
CMD ["python", "app.py"]