from backend.api.db_interactions.delete_data import DeleteData
from backend.api.db_interactions.get_data import GetData
from backend.api.db_interactions.insert_data import InsertData
from backend.api.db_interactions.update_data import UpdateData

import math

from datetime import datetime

class UserSubmissions:
    def __init__(self):
        self.updateData = UpdateData()
        self.insertData = InsertData()
        self.getData = GetData()
        self.deleteData = DeleteData()

    def addWeightLog(self, username, weight):
        try:
            weight = int(weight)
        except ValueError:
            return {"success": False, "message": "Weight is invalid"}
        
        if weight > 2000 or weight < 10:
            return {"success": False, "message": "Weight is invalid"}
        
        return self.insertData.addWeightLog(username, weight)

    def addHeightLog(self, username, height):
        try:
            height = int(height)
        except ValueError:
            return {"success": False, "message": "Height is invalid"}
        
        if height > 240:
            return {"success": False, "message": "Height is invalid"}
        
        return self.insertData.addHeightLog(username, height)

    def updateGoalWeight(self, username, goalWeight):
        try:
            goalWeight = int(goalWeight)
        except ValueError:
            return {"success": False, "message": "Goal weight is invalid"}
        
        if  goalWeight > 2000 or goalWeight < 10:
            return {"success": False, "message": "Goal weight is invalid"}
        
        return self.updateData.updateGoalWeight(username, goalWeight)
    
    def updateGoalDate(self, username, dateStr):
        try:
            date = datetime.strptime(dateStr, "%Y-%m-%d").date()
        except ValueError:
            return {"success": False, "message": "Goal date is invalid"}
        
        if date < datetime.now().date():
            return {"success": False, "message": "Goal date is invalid"}
        
        return self.updateData.updateGoalDate(username, date)

    def changeDOB(self, username, dateStr):
        try:
            date = datetime.strptime(dateStr, "%Y-%m-%d").date()
        except ValueError:
            return {"success": False, "message": "Date of birth is invalid"}
        
        if date > datetime.now().date():
            return {"success": False, "message": "Date of birth must be after today"}

        return self.updateData.updateDob(username, date)

    def calculateInfoAtTime(self, username, date):
        response = self.getData.getDataAtDate(username, date)
        if not response["success"]:
            return response
        data = response["data"]

        if data["weight"] is None or data["height"] is None:
            return {"success": False, "message": "No data on date"}

        dob = datetime.strptime(data["dob"], "%Y-%m-%d").date()
        age = math.floor((date - dob).days / 365)

        daysToGoal = (datetime.strptime(data["goalDate"], "%Y-%m-%d").date() - date).days
        
        BMR = 4.536 * data["weight"] + 15.88 * data["height"] - 5 * age - 78
        
        energyExpenditure = BMR * 1.2

        deficitPerDay = (data["weight"] - data["goalWeight"]) * 3500 / daysToGoal

        calories = max(energyExpenditure - deficitPerDay, 0)
        protein = min(.9 * data["weight"], calories / 4)
        fat = calories * .25 / 9
        carbs = (calories - (protein * 4 + fat * 9)) / 4

        response = self.getData.getCaloriesBurnedOnDate(username, date)

        if not response["success"]:
            return {"success": False, "message": "No data on date"}
        
        if not response["data"]["totalCalsBurned"]:
            calsBurned = 0
        else:
            calsBurned = response["data"]["totalCalsBurned"]

        return {
            "success": True, 
            "data": {
                "calories": calories + calsBurned,
                "protein": protein,
                "carbs": carbs,
                "fat": fat
            }
        }
    
    def insertFoodLog(self, username, foodID, weight, date):
        return self.insertData.insertFoodLog(username, foodID, weight, date)
    
    def insertExerciseLog(self, username, exerciseID, minutes, date):
        return self.insertData.insertExerciseLog(username, exerciseID, minutes, date)
    
    def insertWeightLog(self, username, weight, date):
        return self.insertData.insertWeightLog(username, weight, date)
    
    def insertHeightLog(self, username, height, date):
        return self.insertData.addHeightLog(username, height, date)
    
    def insertExercise(self, name, type, cbpm, musclesWorked):
        if type == 'l':
            return self.insertData.insertLift(name, musclesWorked)
        else:
            return self.insertData.insertCardio(name, cbpm)
        
    def insertFood(self, name, brand, unitCals, unitProtein, unitCarbs, unitFat):
        return self.insertData.insertFood(name, brand, unitCals, unitProtein, unitCarbs, unitFat)
    
    def deleteFoodLog(self, id):
        return self.deleteData.deleteFoodLog(id)
    
    def deleteExerciseLog(self, id):
        return self.deleteData.deleteExerciseLog(id)
    
    def updateDOB(self, username, dob):
        return self.updateData.updateDob(username, dob)
        
    def updateFoodLog(self, logID, newWeight):
        return self.updateData.updateFoodLog(logID, newWeight)

    def updateExerciseLog(self, logID, newTime):
        return self.updateData.updateExerciseLog(logID, newTime)
