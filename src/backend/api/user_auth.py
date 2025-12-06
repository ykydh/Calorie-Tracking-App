#Programmed by Yutaro Kiyota

import hashlib
import re
from backend.api.db_interactions.get_data import GetData
from backend.api.db_interactions.insert_data import InsertData

getData = GetData()
insertData = InsertData()

#Take a password string and hash using SHA-256. Return hashed hex string. 
#parameter type: (password:string) 
def hashPassword(password):
    passwordBinary = password.encode()
    auth = hashlib.sha256()
    auth.update(passwordBinary)
    hashKey = auth.hexdigest()
    return hashKey

def signUpRequest(email, username, password):
    if not isValidEmail(email):
        return {"success": False, "message": "Email is not valid"}
    if not isValidUsername(username):
        return {"success": False, "message": "Username is not valid"}
    
    emailTakenResponse = isEmailTaken(email)
    if not emailTakenResponse["success"]:
        return {"success": False, "message": emailTakenResponse["message"]}
    
    usernameTakenResponse = isUsernameTaken(username)
    if not usernameTakenResponse["success"]:
        return {"success": False, "message": usernameTakenResponse["message"]}

    if emailTakenResponse["taken"]:
        return {"success": False, "message": "Email is already taken"}
    if usernameTakenResponse["taken"]:
        return {"success": False, "message": "Username is already taken"}
    
    hash = hashPassword(password)

    return insertData.addUser(email, username, hash)

def isValidEmail(email):
    return bool(re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email)) and len(email) < 255

def isValidUsername(username):
    return len(username) <= 80

def loginRequest(key, password):
    passHash = None
    if isValidEmail(key):
        response =  getUserWithEmail(key)
    elif isValidUsername(key):
        response =  getUserWithUsername(key)
    else: 
        return {"success": False, "message": "Username/Email is not valid"}
    
    if response["success"]:
            passHash = response["data"]["hash"]
    else: 
        return {"success": False, "message": response["message"]}
    
    if not checkPassword(password, passHash):
        return {"success": False, "message": "Incorrect password"}
    
    data = dict(response["data"])
    del data["hash"]

    return {"success": True, "data": response["data"]}

def getUserWithUsername(username):
    response = getData.getUserWithUsername(username)
    if not response["success"]:
        return {"success": False, "message": response["message"]}
    if response["data"] is None:
        return {"success": False, "message": "Username already registered"}
    return response

def getUserWithEmail(email):
    response = getData.getUserWithEmail(email)
    if not response["success"]:
        return {"success": False, "message": response["message"]}
    if response["data"] is None:
        return {"success": False, "message": "Email already registered"}
    return response

def isUsernameTaken(username):
    response = getData.getUserWithUsername(username)
    if not response["success"]:
        return {"success": False, "message": response["message"]}
    if response["data"] is None:
        return {"success": True, "taken": False}
    else: 
        return {"success": True, "taken": True}
    
def isEmailTaken(email):
    response = getData.getUserWithEmail(email)
    if not response["success"]:
        return {"success": False, "message": response["message"]}
    if response["data"] is None:
        return {"success": True, "taken": False}
    else: 
        return {"success": True, "taken": True}

#checks password user's identity
#Pass a password user input and hashkey retrieved from a user
#parameter type: (password: string, hashKey: string)
def checkPassword(password, hashKey):
    passwordBinary = password.encode()
    auth = hashlib.sha256()
    auth.update(passwordBinary)
    generatedKey = auth.hexdigest()

    if generatedKey == hashKey:
        return True
    else:
        return False

#test
'''
if __name__ == "__main__":
    print("Type your password: ")
    password = input()
    hashedKey = hashPassword(password)
    print(hashedKey)

    print("Input hash key. Assume you got it from a db")
    hashKey = input()
    print("Type ur password: ")
    password = input()
    status = userAuth(password, hashKey)

    if status: 
        print("Success")
    else:
        print("fail")    
'''