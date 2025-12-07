import sqlite3
from backend.api.db_interactions.queries import Queries

class UpdateData:
    def __init__(self):
        self.conn = sqlite3.connect("data.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    # Updates date of birth for specified user 
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

    # Updates goal weight for specified user 
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
        
    # Updates goal date for specified user 
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
        
    # Updates food log for specified user 
    def updateFoodLog(self, logID, newWeight):
        try:
            self.cursor.execute(
                Queries.UPDATE_FOOD_LOG,
                {"logID": logID, "newWeight": newWeight}
            )
            self.conn.commit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    # Updates exercise log for specified user 
    def updateExerciseLog(self, logID, newTime):
        try:
            self.cursor.execute(
                Queries.UPDATE_EXERCISE_LOG,
                {"logID": logID, "newTime": newTime}
            )
            self.conn.commit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}