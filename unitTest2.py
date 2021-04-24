# Before running make sure that db are completely empty,
# different error codes will occur if there exists items which are already in database

import json
from operator import truediv
import requests


def main():
    functional = True
    removeUsers()
    removePosts()
    if not createUsers():   # Creating users for testing
        print("Error Creating Users")
    # Testing if users are not logged in
    if not testMessage() == 401:
        print("Non-Logged-In Message Sending Failed")
        functional = False

    if not testCheckMessages() == 401:
        print("Non-Logged-In Checking Messages Failed")
        functional = False

    if not testCreatePost() == 401:
        print("Non-Logged-In Post Creation Failed")
        functional = False

    if not testReadPost() == 404:
        print("Reading Non-existent Post Failed")
        functional = False

    if not testUpdatePost() >= 400:
        print("Updating Post without Permissions Failed")
        functional = False

    if not testDeletePost() == 401:
        print("Deleting Post without Permissions Failed")
        functional = False

    loginStatus, cookieDict = login()
    # Extracting session cookie to further test in logged in state
    cookie = cookieDict['session']
    if not loginStatus == 200:
        print("Login has failed")
        functional = False
        return

    # Testing after users are logged in #############
    # as long as error code is in 200-300, response is ok
    if not 200 <= testMessage(cookie) < 300:
        print("Logged-In Message Sending Failed")
        functional = False

    if not testCheckMessages(cookie) == 200:
        print("Logged-In Checking Messages Failed")
        functional = False

    if not testCreatePost(cookie) == 200:
        print("Logged-In Post Creation Failed")
        functional = False

    if not testReadPost() == 200:
        print("Reading Existent Post Failed")
        functional = False

    if not testUpdatePost(cookie) == 200:
        print("Updating Post with Permissions Failed")
        functional = False

    if not testDeletePost(cookie) == 204:
        print("Deleting Post with Permissions Failed")
        functional = False

    if functional:
        print("Everything working as intended!")

    removeUsers()   # Removing testing user accounts


def testMessage(cookie=None):
    url = "http://localhost:5000/api/message/unittest2user2"

    payload = json.dumps({
        "content": "testingmessage"
    })

    if cookie == None:
        headers = {
            'Content-Type': 'application/json'
        }
    else:
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'session=' + cookie
        }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code


def testCheckMessages(cookie=None):
    url = "http://localhost:5000/api/checkmessages"

    payload = ""
    if cookie == None:
        headers = {
            'Content-Type': 'application/json'
        }
    else:
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'session=' + cookie
        }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.status_code


def testCreatePost(cookie=None):
    url = "http://localhost:5000/api/createpost"

    payload = json.dumps({
        "content": "lorem imposum dolorarrs"
    })
    if cookie == None:
        headers = {
            'Content-Type': 'application/json'
        }
    else:
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'session=' + cookie
        }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code


def testReadPost():
    url = "http://localhost:5000/api/readpost/1"

    payload = json.dumps({
        "content": "lorem imposum dolorarrs"
    })
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.status_code


def testUpdatePost(cookie=None):
    url = "http://localhost:5000/api/updatepost/1"

    payload = json.dumps({
        "content": "new content"
    })
    if cookie == None:
        headers = {
            'Content-Type': 'application/json'
        }
    else:
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'session=' + cookie
        }

    response = requests.request("PUT", url, headers=headers, data=payload)
    return response.status_code


def testDeletePost(cookie=None):
    url = "http://localhost:5000/api/deletepost/1"

    payload = json.dumps({
        "content": "lorem imposum dolorarrs"
    })
    if cookie == None:
        headers = {
            'Content-Type': 'application/json'
        }
    else:
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'session=' + cookie
        }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    return response.status_code


def login():
    url = "http://localhost:5000/api/login"

    payload = json.dumps({
        "username": "unittest2user1",
        "password": "pw",
    })
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return (response.status_code, response.cookies.get_dict())


def createUsers():
    url = "http://localhost:5000/api/signup"

    payload = json.dumps({
        "username": "unittest2user1",
        "password": "pw"
    })
    headers = {
        'Content-Type': 'application/json',
    }

    response1 = requests.request("POST", url, headers=headers, data=payload)

    payload = json.dumps({
        "username": "unittest2user2",
        "password": "pw"
    })
    headers = {
        'Content-Type': 'application/json',
    }

    response2 = requests.request("POST", url, headers=headers, data=payload)

    if response1.status_code == 201 and response2.status_code == 201:
        return True
    else:
        return False


def removeUsers():
    url = "http://localhost:5000/api/deluser/unittest2user1"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJydjktuwzAMRK8icG0Upijr41N0XwQBZZKxAbcJLGcV5O4V0Bt0RZDDmXkvuNrObdUG89cL3NkHfGtrfFMY4HNXbur2-81tP-68O16WLrpz3Zp79J8PuLyHf_ouQy8_tK0wn8dT-7YJzFCRSglFa8JQgq8aqtG4EE1SfUjIyJp1CoZj4mzKKKEIWiEbo6FniT5LiZ44YY9I4rXfMwpVs5JIapSkRjFRqNw9OWQd_UTGOUrs-Ndn0-OPBuH9Cxa6WLw.YIM_Qw.RrDjUwT6Zp_rnnuLnYVetD8j1Xg'
    }

    response1 = requests.request("DELETE", url, headers=headers, data=payload)

    url = "http://localhost:5000/api/deluser/unittest2user2"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJydjktuwzAMRK8icG0Upijr41N0XwQBZZKxAbcJLGcV5O4V0Bt0RZDDmXkvuNrObdUG89cL3NkHfGtrfFMY4HNXbur2-81tP-68O16WLrpz3Zp79J8PuLyHf_ouQy8_tK0wn8dT-7YJzFCRSglFa8JQgq8aqtG4EE1SfUjIyJp1CoZj4mzKKKEIWiEbo6FniT5LiZ44YY9I4rXfMwpVs5JIapSkRjFRqNw9OWQd_UTGOUrs-Ndn0-OPBuH9Cxa6WLw.YIM_Qw.RrDjUwT6Zp_rnnuLnYVetD8j1Xg'
    }

    response2 = requests.request("DELETE", url, headers=headers, data=payload)

    if response1.status_code == 204 and response2.status_code == 204:
        return True
    else:
        return False


def removePosts():
    pass


main()
