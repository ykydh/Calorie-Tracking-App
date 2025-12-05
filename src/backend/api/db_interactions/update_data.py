import sqlite3
from backend.api.db_interactions.queries import Queries

class UpdateData:
    def __init__(self):
        self.conn = sqlite3.connect("data.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    def updateWeight(self, username, weight):
        try:
            self.cursor.execute(
                Queries.UPDATE_WEIGHT,
                {"weight": weight, "username": username}
            )
            self.conn.commit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}
    def updateHeight(self, username, height):
        try:
            self.cursor.execute(
                Queries.UPDATE_HEIGHT,
                {"weight": height, "username": username}
            )
            self.conn.commit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def updateDob(self, username, date):
        try:
            self.cursor.execute(
                Queries.UPDATE_DOB,
                {"weight": date, "username": username}
            )
            self.conn.commit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def updateGoalWeight(self, username, goalWeight):
        try:
            self.cursor.execute(
                Queries.UPDATE_GOAL_WEIGHT,
                {"weight": goalWeight, "username": username}
            )
            self.conn.commit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}