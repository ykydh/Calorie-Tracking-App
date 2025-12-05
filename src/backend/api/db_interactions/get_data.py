import sqlite3
from backend.api.db_interactions.queries import Queries

class GetData:
    def __init__(self):
        self.conn = sqlite3.connect("data.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        
    def getUserWithUsername(self, username):
        try:
            self.cursor.execute(Queries.GET_USER_FROM_USERNAME, {"username": username})
            data = self.cursor.fetchone()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def getUserWithEmail(self, email):
        try:
            self.cursor.execute(Queries.GET_USER_FROM_EMAIL, {"email": email})
            data = self.cursor.fetchone()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": str(e)}
    