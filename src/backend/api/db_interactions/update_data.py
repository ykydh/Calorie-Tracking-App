import sqlite3
from backend.api.db_interactions.queries import Queries

class UpdateData:
    def __init__(self):
        self.conn = sqlite3.connect("data.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    def updateDob(self, username, date):
        try:
            self.cursor.execute(
                Queries.UPDATE_DOB,
                {"dob": date, "username": username}
            )
            self.conn.commit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def updateGoalWeight(self, username, goalWeight):
        try:
            self.cursor.execute(
                Queries.UPDATE_GOAL_WEIGHT,
                {"goalWeight": goalWeight, "username": username}
            )
            self.conn.commit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    def updateGoalDate(self, username, goalDate):
        try:
            self.cursor.execute(
                Queries.UPDATE_GOAL_DATE,
                {"goalDate": goalDate, "username": username}
            )
            self.conn.commit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}