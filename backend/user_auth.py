#Programmed by Yutaro Kiyota

import hashlib


#Take a password string and hash using SHA-256. Return hashed hex string. 
#parameter type: (password:string) 
def hashPassword(password):
    passwordBinary = password.encode()
    auth = hashlib.sha256()
    auth.update(passwordBinary)
    hashKey = auth.hexdigest()
    return hashKey

#Authenticate user's identity
#Pass a password user input and hashkey retrieved from a user
#parameter type: (password: string, hashKey: string)
def userAuth(password, hashKey):
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