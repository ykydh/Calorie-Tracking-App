from backend.api.db_interactions.delete_data import DeleteData
from backend.api.db_interactions.get_data import GetData
from backend.api.db_interactions.insert_data import InsertData
from backend.api.db_interactions.update_data import UpdateData

from datetime import datetime

class UserSubmissions:
    def __init__(self):
        self.updateData = UpdateData()
        self.insertData = InsertData()
        self.getData = GetData()
        self.deleteData = DeleteData()

    def updateWeight(self, username, weight):
        try:
            weight = int(weight)
        except ValueError:
            return {"success": False, "message": "Weight is invalid"}
        
        if weight > 2000 or weight < 10:
            return {"success": False, "message": "Weight is invalid"}
        
        return self.updateData.updateWeight(username, weight)

    def updateHeight(self, username, height):
        try:
            height = int(height)
        except ValueError:
            return {"success": False, "message": "Height is invalid"}
        
        if height > 240:
            return {"success": False, "message": "Height is invalid"}
        
        return self.updateData.updateHeight(username, height)

    def updateGoalWeight(self, username, goalWeight):
        try:
            goalWeight = int(goalWeight)
        except ValueError:
            return {"success": False, "message": "Goal weight is invalid"}
        
        if  goalWeight > 2000 or goalWeight < 10:
            return {"success": False, "message": "Goal weight is invalid"}
        
        return self.updateData.updateGoalWeight(username, goalWeight)

    def changeDOB(self, username, dateStr):
        try:
            date = datetime.strptime(dateStr, "%Y-%m-%d").date()
        except ValueError:
            return {"success": False, "message": "Date is invalid"}

        return self.updateData.updateDob(username, date)