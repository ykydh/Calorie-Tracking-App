import sqlite3
from backend.api.db_interactions.queries import Queries

class DeleteData:
    def __init__(self, conn=None):
        self.conn = conn or sqlite3.connect("data.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  
        
        # Enable safety settings
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.execute("PRAGMA journal_mode = WAL;")
        self.conn.execute("PRAGMA busy_timeout = 3000;")
        
    def deleteFoodLog(self, id):
        try:
            with self.conn:
                self.conn.execute(
                    Queries.DELETE_FOOD_LOG,
                    {"id": id}
                )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": e}
        
    def deleteExerciseLog(self, id):
        try:
            with self.conn:
                self.conn.execute(
                    Queries.DELETE_EXERCISE_LOG,
                    {"id": id}
                )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": e}