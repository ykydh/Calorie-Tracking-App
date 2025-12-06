from database import createDatabase, clearDatabase, initalizeDatabase

try:
    clearDatabase()
    createDatabase()
    initalizeDatabase()
    print("SUCCESSFULLY CREATED")
except Exception as e:
    clearDatabase()
    raise(e)