# Environment Setup Instructions

This guide outlines the steps necessary to set up your development environment for the project. Please follow the instructions in the order provided.

## Prerequisites

Before you begin, ensure you have Docker and Python 3 installed on your machine. These tools are required to execute the setup steps.


## Step 1: Set Up the Django Application

1. **Prepare Django Migrations**:
   
    Before running the application, you need to prepare the database migrations. Use Docker Compose to run the migration commands within the containerized environment:

    ```sh
    docker-compose run web python3 Rag_persona/manage.py makemigrations
    docker-compose run web python3 Rag_persona/manage.py migrate
    ```

    These commands generate the necessary database migration files and apply them, setting up the database schema.

## Step 2: Launch the Application

1. **Start the Application**:

    Finally, start your Dockerized application. Ensure the Docker daemon is running, and execute the following command:

    ```sh
    docker-compose -f docker-compose.yml --env-file .env up -d --build
    ```

    This command tells Docker Compose to use your `docker-compose.yml` and `.env` configuration files to build and start the application containers in detached mode.

    After the containers are up and running, your Django application should be accessible.

# API EndPoints
Here, I assume port 8000 is mapped.
```sh
import requests, json
```
## Create User
**ONLY EMAIL AND PASSWORD INPUTS ARE REQUIRED**

```sh
endpoint = "http://localhost:8000/api/createuser/"
data = {
   email: placeholder@gmail.com,
   password: password,
   first_name: first,
   second_name: second,
   username: first_second
}

requests.post(endpoint,
   headers={
   "Content-Type": "application/json"},
   json=data
)
```

## Authentication
**Authentication is done using [Django rest framework JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)**

```sh

#token auth
endpoint_auth = "http://localhost:8000/api/token/"
data = {
   email: placeholder@gmail.com,
   password: password,
}
response = requests.post(endpoint_auth, json = data)

# token refresh
endpoint_refresh = "http://localhost:8000/api/token/refresh/"
data = {
   'refresh': #$%^^&%KKOJO
}
response = requests.post(endpoint_auth, json = data)

```
__response.json() in both instances is a dictionary with 'refresh' and 'access' as dictionary keys__





