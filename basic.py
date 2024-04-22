import requests, json
from getpass import getpass

endpoint_list = "http://localhost:8000/api/"
endpoint_auth= "http://localhost:8000/api/token/"
refresh = "http://localhost:8000/api/token/refresh/"
endpoint_prompt= "http://localhost:8000/api/query/"

username = 'oguntoyek@gmail.com' #input("Username: ")
username = 'oguntoye@iastate.edu'
password = 'Mo444mo4o'  #getpass("Password: ")

# get = requests.post(endpoint)

get = requests.post(endpoint_auth, json={"email": username,
                                        "password": password})


tmp = {
    "refresh": get.json().get('refresh'),
}
# get = requests.post(refresh, json=tmp)
# print(get.json())
# data = {
#     "query": "using the way i wrote past emails, write an email to Dr Kyle asking for a letter of recommendation. What should I",
# }


# email = "ogunty@gmail.com"
# password ="Mo444mo4o"
# first_name = "Oluwaseun"
# last_name = "Oguntoye"
# username = "scoffied"

# post_data = {
#     "email": email,
#     "password": password,
#     # "first_name": first_name,
#     # "last_name": last_name,
#     # "username": username
# }
# endpoint = endpoint_prompt= "http://localhost:8000/api/createuser/"
# requests.post(endpoint,
#    headers={
#    "Content-Type": "application/json"},
#    json=post_data
# )


#DEMO BEFORE AND AFTER DATABASE UPDATE.
data = {
    "query": "what is my opinion about Trump?",
    }

# post_doc = {
#     "text": "I need habanero, so i have to go and get it."
# }

# print(get.json())

# data = {
#    "text": """
#       In the heart of night, under a velvet sky,
#       Whispers of the moon, on a breeze, softly lie.
#       Stars, like scattered dreams, in darkness dance,
#       Weaving tales in silence, as if by chance.
#       """

# }

# data = {
#      "query": "what happens at night?",
#      }

if get.status_code == 200:
    token = get.json()['access']
    # print(token)
    get = requests.post(endpoint_prompt,
                       headers={"Authorization": f"Bearer {token}"},
                        data=data)
    print(get)
else:
    print("Authentication failed")

# if get.status_code == 200:

#     token = get.json()['access']

#     #POST data to the user's database
#     # get = requests.post(endpoint_list,
#     #                    headers={"Authorization": f"Bearer {token}",
#     #                             "Content-Type": "application/json"},
#     #                    json=data)

#     #GET all data connected to the user
#     get = requests.get(endpoint_list,
#                     headers={"Authorization": f"Bearer {token}"})

#     print(get.json())
# else:
#     print("Authentication failed")