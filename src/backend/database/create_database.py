from database import createDatabase, clearDatabase, initalizeDatabase, test

try:
    clearDatabase()
    createDatabase()
    initalizeDatabase()
    print("SUCCESSFULLY CREATED")
except Exception as e:
    clearDatabase()
    raise(e)