from database import createDatabase

try:
    createDatabase()
    print("SUCCESSFULY CREATED")
except Exception as e:
    print(str(e))