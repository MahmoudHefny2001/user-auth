# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /E-Commerce-Graduation-Project
WORKDIR /E-Commerce-Graduation-Project


# env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Copy the work directory contents into the container at /E-Commerce-Graduation-Project

# RUN  cd ..

ADD . /E-Commerce-Graduation-Project

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set execute permissions on the entrypoint script
RUN chmod +x entrypoint.sh

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Apply database migrations
RUN python3 manage.py makemigrations && python3 manage.py migrate

# Run django-admin startproject myproject when the container launches
CMD ["sh", "entrypoint.sh"]

