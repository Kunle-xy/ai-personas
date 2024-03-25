STEP 1:
docker-compose run web python3 Rag_persona/manage.py makemigrations
docker-compose run web python3 Rag_persona/manage.py migrate

STEP 2:
docker-compose  -f docker-compose.yml --env-file .env up -d --build
