
# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8
RUN python -m pip install --upgrade pip
# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /api_service

# Set the working directory to /music_service
WORKDIR /api_service

# Copy the current directory contents into the container at /music_service
ADD . /api_service/
    
ENV PIP_ROOT_USER_ACTION=ignore
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir  -r requirements.txt