# Unit testing for user signup and login
import requests
import json


def main():

    functional = True
    if not testSignup():
        print("Signup Function Failed")
        functional = False
    if not testLogin():
        print("Login Function Failed")
        functional = False
    if not testLogout():
        print('Logout Function Failed')
        functional = False

    removeTestUser()  # Cleaning up after
    print("Login and Signup functions work: ", functional)


def testSignup():
    # Clearing previous user
    removeTestUser()

    # Testing signup
    url = "http://localhost:5000/api/signup"

    payload = "{\r\n\t\"username\": \"unittest1\",\r\n\t\"password\": \"unittest1pw\"\r\n}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 201:
        return True
    else:
        return False


def testLogin():
    # Testing login logic
    url = "http://localhost:5000/api/login"
    payload = "{\r\n\t\"username\": \"unittest1\",\r\n\t\"password\": \"unittest1pw\"\r\n}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return True
    else:
        return False


def testLogout():
    url = "http://localhost:5000/api/logout"

    payload = ""
    headers = {
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        return True
    else:
        return False


def removeTestUser():
    # Clearing users if there exists one before
    url = "http://localhost:5000/api/deluser/unittest1"

    payload = "{\r\n\t\"username\": \"unittest1\",\r\n\t\"password\": \"unittest1pw\"\r\n}"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


main()
