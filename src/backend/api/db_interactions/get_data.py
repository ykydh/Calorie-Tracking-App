import sqlite3
from backend.api.db_interactions.queries import Queries
from backend.objects.food_log import FoodLog
from backend.objects.exercise.cardio import Cardio
from backend.objects.exercise.lift import Lift

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
            return {"success": False, "message": e}
    
    def getUserWithEmail(self, email):
        try:
            self.cursor.execute(Queries.GET_USER_FROM_EMAIL, {"email": email})
            data = self.cursor.fetchone()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": e}
    
    def getFoodLogsWithInfo(self, username, date):
        logsWithInfo = []

        try:
            self.cursor.execute(Queries.GET_FOOD_LOGS, {"username": username , "date": date})
            logs = self.cursor.fetchall()
            for log in logs:
                self.cursor.execute(Queries.GET_LOG_INFO, {"logID": log["logID"]})
                logInfo = self.cursor.fetchone()
                foodLog = FoodLog(
                    log["logID"],
                    logInfo["name"],
                    logInfo["brand"],
                    logInfo["weight"],
                    logInfo["logCalories"],
                    logInfo["logProtein"],
                    logInfo["logCarbs"],
                    logInfo["logFat"]
                )
                logsWithInfo.append(foodLog)

            return {"success": True, "data": logsWithInfo}
        except Exception as e:
            return {"success": False, "message": e}

    def getDailyTotals(self, username, date):
        try:
            self.cursor.execute(Queries.GET_DAILY_INFO, {"username": username , "date": date})
            data = self.cursor.fetchone()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": e}
        
    def getDataAtDate(self, username, date):
        try:
            self.cursor.execute(Queries.GET_USER_INFO_AT_TIME, {"username": username , "date": date})
            data = self.cursor.fetchone()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": e}
        
    def getFoodLogsOnDate(self, username, date):
        try:
            self.cursor.execute(Queries.GET_USER_INFO_AT_TIME, {"username": username , "date": date})
            data = self.cursor.fetchone()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": e}
        
    def getFoodLike(self, brand, name):
        try:
            self.cursor.execute(Queries.GET_FOODS_LIKE, {"brand": brand, "name": name})
            data = self.cursor.fetchall()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": e}
        
    def getExerciseLogs(self, username, date):
        try:
            self.cursor.execute(Queries.GET_EXERCISE_LOGS_ON, {"username": username, "date": date})
            logs = self.cursor.fetchall()
            exercises = []
            for log in logs:
                if log["type"] == 'c':
                    self.cursor.execute(Queries.GET_CARDIO, {"id": log["exerciseID"]})
                    cardioInfo = self.cursor.fetchone()
                    exercises.append(
                        Cardio (
                            log["minutes"],
                            cardioInfo["name"],
                            log["exerciseID"],
                            cardioInfo["cbpm"],
                            log["logID"]
                        )
                    )
                elif log["type"] == 'l':
                    self.cursor.execute(Queries.GET_LIFT, {"id": log["exerciseID"]})
                    liftInfo = self.cursor.fetchone()
                    exercises.append(
                        Lift (
                            log["minutes"],
                            liftInfo["name"],
                            log["exerciseID"],
                            liftInfo["musclesWorked"],
                            log["logID"]
                        )
                    )
            return {"success": True, "data": exercises}
        except Exception as e:
            return {"success": False, "message": e}
        
    def getCaloriesBurnedOnDate(self, username, date):
        try:
            self.cursor.execute(Queries.GET_CALORIES_BURNED_ON, {"username": username, "date": date})
            data = self.cursor.fetchone()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": e}
        
    def getExercisesLike(self, name):
        try:
            self.cursor.execute(Queries.GET_EXERCISES_LIKE, {"name": name})
            data = self.cursor.fetchall()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": e}
        
    def getWeightLogs(self, username):
        try:
            self.cursor.execute(Queries.GET_WEIGHT_LOGS, {"username": username})
            data = self.cursor.fetchall()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": e}
        
    def getDobAndHeight(self, username):
        try:
            self.cursor.execute(Queries.GET_DOB_AND_HEIGHT, {"username": username})
            data = self.cursor.fetchone()
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": e}