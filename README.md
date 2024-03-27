#Set-up 

##Environment set up
### Step 1
`python3 -m venv env`
`pip install -r requirements.txt`



STEP 1:
docker-compose run web python3 Rag_persona/manage.py makemigrations
docker-compose run web python3 Rag_persona/manage.py migrate

STEP 2:
docker-compose  -f docker-compose.yml --env-file .env up -d --build
