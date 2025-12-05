import sqlite3
from backend.api.db_interactions.queries import Queries

class InsertData:
    def __init__(self):
        self.conn = sqlite3.connect("data.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
    
    def add_user(self, email, username, hash):
        try:
            self.cursor.execute(
                Queries.INSERT_USER_TO_ACCOUNT,
                {
                    "email": email,
                    "username": username,
                    "hash": hash
                }
            )

            self.cursor.execute(
                Queries.INSERT_USER_TO_USER,
                {"username": username}
            )

            self.conn.commit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}