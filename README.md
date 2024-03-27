# Environment Setup Instructions

This guide outlines the steps necessary to set up your development environment for the project. Please follow the instructions in the order provided.

## Prerequisites

Before you begin, ensure you have Docker and Python 3 installed on your machine. These tools are required to execute the setup steps.

## Step 1: Prepare the Python Environment

1. **Create a Virtual Environment**: Isolate your project dependencies by creating a virtual environment. Open your terminal and run:

    ```sh
    python3 -m venv env
    ```

2. **Activate the Virtual Environment**: Before installing the project dependencies, activate the virtual environment:

    - On Windows:
        ```cmd
        .\env\Scripts\activate
        ```
    - On Unix or MacOS:
        ```sh
        source env/bin/activate
        ```

3. **Install Dependencies**: With the virtual environment activated, install the project dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Step 2: Set Up the Django Application

1. **Prepare Django Migrations**:
   
    Before running the application, you need to prepare the database migrations. Use Docker Compose to run the migration commands within the containerized environment:

    ```sh
    docker-compose run web python3 Rag_persona/manage.py makemigrations
    docker-compose run web python3 Rag_persona/manage.py migrate
    ```

    These commands generate the necessary database migration files and apply them, setting up the database schema.

## Step 3: Launch the Application

1. **Start the Application**:

    Finally, start your Dockerized application. Ensure the Docker daemon is running, and execute the following command:

    ```sh
    docker-compose -f docker-compose.yml --env-file .env up -d --build
    ```

    This command tells Docker Compose to use your `docker-compose.yml` and `.env` configuration files to build and start the application containers in detached mode.

    After the containers are up and running, your Django application should be accessible.
