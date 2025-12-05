import sqlite3
from queries import Queries

class GetData:
    def __init__(self):
        self.conn = sqlite3.connect("data.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        
    def getPasswordWithUsername(self, username):
        self.cursor.execute(Queries.GET_PASSWORD_FROM_USERNAME, {"username": username})
        return self.cursor.fetchone()
    
    def getPasswordWithUsername(self, email):
        self.cursor.execute(Queries.GET_PASSWORD_FROM_USERNAME, {"email": email})
        return self.cursor.fetchone()