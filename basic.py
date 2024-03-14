import requests, json
from getpass import getpass

endpoint_list = "http://localhost:8000/api/"
endpoint_auth= "http://localhost:8000/api/token/"
endpoint_prompt= "http://localhost:8000/api/query/"

username = 'oguntoye@iastate.edu' #input("Username: ")
password = 'Mo444mo4o'  #getpass("Password: ")

# get = requests.post(endpoint)

get = requests.post(endpoint_auth, json={"email": username,
                                        "password": password})

data = {
    "query": "using the way i wrote past emails, write an email to Dr Kyle asking for a letter of recommendation. What should I",
}

post_doc = {
    "text": "I need habanero, so i have to go and get it."
}

# print(get.json())

if get.status_code == 200:
    token = get.json()['access']
    get = requests.post(endpoint_prompt,
                       headers={"Authorization": f"Bearer {token}"},
                        data=data)
    print(get.json())
else:
    print("Authentication failed")

# if get.status_code == 200:

#     token = get.json()['access']

#     #POST data to the user's database
#     get = requests.post(endpoint_list,
#                        headers={"Authorization": f"Bearer {token}",
#                                 "Content-Type": "application/json"},
#                        json=post_doc)

#     #GET all data connected to the user
#     # get = requests.get(endpoint_list,
#     #                 headers={"Authorization": f"Bearer {token}"})

#     print(get.json())
# else:
#     print("Authentication failed")