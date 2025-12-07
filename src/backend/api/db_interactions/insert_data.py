import sqlite3
from backend.api.db_interactions.queries import Queries
from datetime import datetime

class InsertData:
    def __init__(self, conn=None):
        # Allow one shared connection OR create one if not provided
        self.conn = conn or sqlite3.connect("data.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  
        
        # Enable safety settings
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.execute("PRAGMA journal_mode = WAL;")
        self.conn.execute("PRAGMA busy_timeout = 3000;")

    # Adds user to both account and user tables
    def addUser(self, email, username, hash):
        try:
            with self.conn:
                self.conn.execute(
                    Queries.INSERT_USER_TO_ACCOUNT,
                    {"email": email, "username": username, "hash": hash}
                )
                self.conn.execute(
                    Queries.INSERT_USER_TO_USER,
                    {"username": username}
                )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # Adds weight log for a user
    def addWeightLog(self, username, weight):
        try:
            with self.conn:
                self.conn.execute(
                    Queries.INSERT_WEIGHT_LOG,
                    {"weight": weight, "username": username, "date": datetime.now().date()}
                )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # Adds height log for a user
    def addHeightLog(self, username, height):
        try:
            with self.conn:
                self.conn.execute(
                    Queries.INSERT_HEIGHT_LOG,
                    {"height": height, "username": username, "date": datetime.now().date()}
                )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # Inserts a food log for specified user
    def insertFoodLog(self, username, foodID, weight, date):
        try:
            with self.conn:
                self.conn.execute(
                    Queries.INSERT_FOOD_LOG,
                    {"username": username, "foodID": foodID, "weight": weight, "date": date}
                )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    # Inserts exercise log for specified user
    def insertExerciseLog(self, username, exerciseID, minutes, date):
        try:
            with self.conn:
                self.conn.execute(
                    Queries.INSERT_EXERCISE_LOG,
                    {"username": username, "exerciseID": exerciseID, "minutes": minutes, "date": date}
                )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    # Inserts weight log for specified user
    def insertWeightLog(self, username, weight, date):
        try:
            with self.conn:
                self.conn.execute(
                    Queries.INSERT_WEIGHT_LOG,
                    {"username": username, "weight": weight,"date": date}
                )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    # Inserts lift
    def insertLift(self, name, musclesWorked):
        try:
            with self.conn:
                self.conn.execute(
                    Queries.INSERT_LIFT,
                    {"name": name, "musclesWorked": musclesWorked}
                )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # Inserts cardio
    def insertCardio(self, name, cbpm):
        try:
            with self.conn:
                self.conn.execute(
                    Queries.INSERT_CARDIO,
                    {"name": name, "cbpm": cbpm}
                )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    # Inserts food
    def insertFood(self, name, brand, unitCals, unitProtein, unitCarbs, unitFat):
        try:
            with self.conn:
                self.conn.execute(
                    Queries.INSERT_FOOD,
                    {
                        "name": name,
                        "brand": brand,
                        "unitCals": unitCals,
                        "unitProtein": unitProtein,
                        "unitCarbs": unitCarbs,
                        "unitFat": unitFat
                    }
                )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}