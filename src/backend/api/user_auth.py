#Programmed by Yutaro Kiyota

import hashlib
import re
from src.backend.api.db_interactions.get_data import GetData


#Take a password string and hash using SHA-256. Return hashed hex string. 
#parameter type: (password:string) 
def hashPassword(password):
    passwordBinary = password.encode()
    auth = hashlib.sha256()
    auth.update(passwordBinary)
    hashKey = auth.hexdigest()
    return hashKey

def isValidEmail(email):
    return bool(re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email))

def authUser(key, password):
    passHash = None
    if isValidEmail(key):
        response =  getPasswordWithEmail(key)
        if response["success"]:
            passHash = response["passHash"]
        else: 
            return {"success": False, "message": "Email is not registered"}
    else:
        response =  getPasswordWithUsername(key)
        if response["success"]:
            passHash = response["passHash"]
        else: 
            return {"success": False, "message": "Username is not registered"}
    if not checkPassword(password, passHash):
        return {"success": False, "message": "Incorrect password"}
    return {"success": True}

def getPasswordWithUsername(username):
    return GetData.getPasswordWithUsername(username)

def getPasswordWithEmail(email):
    return GetData.getPasswordWithEmail(email)

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