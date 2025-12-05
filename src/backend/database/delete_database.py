from database import clearDatabase

try:
    clearDatabase()
    print("SUCCESSFULY CLEARED")
except Exception as e:
    print(str(e))