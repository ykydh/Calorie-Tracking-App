import sqlite3
from backend.api.db_interactions.queries import Queries
from backend.objects.food_log import FoodLog

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
    
    def getFoodLogsWithInfo(self, username, date):
        logsWithInfo = []

        try:
            self.cursor.execute(Queries.GET_FOOD_LOGS, {"username": username , "date": date})
            logs = self.cursor.fetchall()

            for log in logs:
                self.cursor.execute(Queries.GET_LOG_INFO, {"logID": log["logID"]})
                logInfo = self.cursor.fetchone()
                logsWithInfo.append(
                    FoodLog(
                        log["logID"],
                        logInfo["name"],
                        logInfo["brand"],
                        logInfo["weight"],
                        logInfo["logCalories"],
                        logInfo["logProtein"],
                        logInfo["logCarbs"],
                        logInfo["logFat"]
                    )
                )
            return {"success": True, "data": logsWithInfo}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def getDailyTotals(self, username, date):
        try:
            self.cursor.execute(Queries.GET_DAILY_INFO, {"username": username , "date": date})
            data = self.cursor.fetchone()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    def getDataAtDate(self, username, date):
        try:
            self.cursor.execute(Queries.GET_USER_INFO_AT_TIME, {"username": username , "date": date})
            data = self.cursor.fetchone()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    def getFoodLogsOnDate(self, username, date):
        try:
            self.cursor.execute(Queries.GET_USER_INFO_AT_TIME, {"username": username , "date": date})
            data = self.cursor.fetchone()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": str(e)}