from backend.objects.exercise.exercise import Exercise

class Lift(Exercise):
    def __init__(self, minutes, name, id, musclesWorked, logID):
        super().__init__(minutes, name, id, logID)
        self.musclesWorked = musclesWorked

    def getInfo(self):
        return f"Muscles worked: {self.musclesWorked}"