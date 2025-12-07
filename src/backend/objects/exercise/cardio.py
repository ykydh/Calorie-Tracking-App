from backend.objects.exercise.exercise import Exercise

class Cardio(Exercise):
    def __init__(self, minutes, name, id, cbpm, logID):
        super().__init__(minutes, name, id, logID)
        self.cbpm = cbpm

    def getInfo(self):
        return f"Calories burned: {self.minutes * self.cbpm}"