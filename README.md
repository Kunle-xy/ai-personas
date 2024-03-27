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
    docker-compose run web python3 Rag_persona/manage.py createsuperuser
    # creatine super user requires email and password input

    #creating a superuser account allows you to access the admin website provided by Django and to view all users and documents provided by users.
    ```

    These commands generate the necessary database migration files and apply them, setting up the database schema.

## Step 2: Launch the Application

1. **Start the Application**:

    Finally, start your Dockerized application. Ensure the Docker daemon is running, and execute the following command:

Start the Docker Compose services in detached mode with a custom `.env` file, and build images as necessary:
    ```
    docker-compose -f docker-compose.yml --env-file .env up -d --build
    ```

 Wait for a moment to allow the services to start up. Then, to check the logs of the services to ensure everything is running smoothly:
    ```
    docker-compose logs
    ```

After confirming the application has started successfully, access the admin page by navigating to [http://localhost:8000/admin/](http://localhost:8000/admin/) in your web browser and log in with your credentials to manage the application.


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


## Add data to Database
**This endpoint performs CREATE and READ using post and get requests, respectively**

```sh

# Create new data to user's database

endpoint_data = "http://localhost:8000/api/"
endpoint_auth = "http://localhost:8000/api/token/"

data = {
   "text": """
      In the heart of night, under a velvet sky,
      Whispers of the moon, on a breeze, softly lie.
      Stars, like scattered dreams, in darkness dance,
      Weaving tales in silence, as if by chance.
      """

}
response = requests.post(endpoint_auth, json = data)
token = response.json()['access']
response = requests.post(endpoint_data,
                     headers={"Authorization": f"Bearer {token}",
                              "Content-Type": "application/json"},
                      json=post_doc)

# Response returns a dictionary with keys listed in ~ ['uploaded_at', 'topic', 'vector', 'text']
# topic is the first sentence
# vector is the word embeddings
# text as it
# uploaded_at is the date created

# List all user's data
response = requests.get(endpoint_data,
                headers={"Authorization": f"Bearer {token}"})

# response format ditto

```

## Text Generation and Question/Answering

``` sh
   data = {
     "query": "Write a poem about a Bentley car using my style?"
     }
   # token is generated using a similar call from the above function calls.
   response = requests.post(endpoint_prompt,
                     headers={"Authorization": f"Bearer {token}"},
                     data=data)
                     
   print(response.json())
```






