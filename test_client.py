import requests as rq
from crewco_api.api import API

api = API()


def auth(name, password):
    url = 'http://127.0.0.1:5000/api/auth'
    data = {"name": api.encrypt(name).decode(), "key": api.encrypt(password).decode()}

    response = rq.post(url, json=data)

    try:
        response_json = response.json()
        status = response_json.get('status')
        if status == 'ok':
            return "Authentication successful"
        else:
            return "Authentication failed"
    except rq.exceptions.JSONDecodeError:
        return "Invalid response format"


def lookup(name):
    url = 'http://127.0.0.1:5000/api/lookup'
    data = {"name": name}
    res = rq.post(url, json=data)

    try:
        response_json = res.json()
        return response_json
    except rq.exceptions.JSONDecodeError:
        return None


# Main program
name = input("name: ")
password = input("password: ")

if auth(name, password) == "Authentication successful":
    lookup_name = input("Lookup> ")
    lookup_result = lookup(api.encrypt(lookup_name).decode())
    lookup_result_formatted = f"Name:{lookup_result['Name']}\nAge:{lookup_result['Age']}\nLocation{lookup_result['Country']}"

    if lookup_result is not None:
        print(lookup_result_formatted)
    else:
        print("Invalid response format for lookup")
else:
    print("Authentication failed")
