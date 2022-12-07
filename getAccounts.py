import json

def getAdminAccount():
    
    with open("./Data/admins.json", "r") as file:
        JSON = file.read()

    accounts = json.loads(JSON)

    return accounts


def getAccount():
    
    with open("./Data/accounts.json", "r") as file:
        JSON = file.read()

    accounts = json.loads(JSON)

    return accounts



