import customtkinter as ctk
from GUI.authentication.welcome import WelcomeScreen
from GUI.authentication.login import LoginScreen
from GUI.authentication.sign_up import SignUpScreen
from GUI.dashboard.dashboard import Dashboard
from GUI.auxillary.biometrics import Biometrics
from GUI.dashboard.elements.insert_exercise_log import InsertExerciseLog
from GUI.dashboard.elements.insert_exercise import InsertExercise
from GUI.dashboard.elements.insert_food_log import InsertFoodLog
from GUI.dashboard.elements.insert_food import InsertFood
from GUI.dashboard.elements.insert_weight_log import InsertWeightLog
from GUI.dashboard.elements.profile import Profile
from datetime import datetime

class CalorieTrackingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Calorie App")
        self.minsize(600,475)
        
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True)
        
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=1)
        
        self.username = None
        self.selectedDate = datetime.now().date()
        
        self.frames = {}
        for ScreenClass in (WelcomeScreen, LoginScreen, SignUpScreen, Dashboard, Biometrics, InsertExerciseLog, InsertFoodLog, InsertWeightLog, InsertExercise, InsertFood, Profile):
            frame = ScreenClass(main, self)
            self.frames[ScreenClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        
        self.bind("<Return>", self.handleEnter)

        self.currFrame = None
        self.showFrame("WelcomeScreen")

    def showFrame(self, name):
        frame = self.frames[name]
        frame.tkraise()

        if hasattr(self.currFrame, "clearInput"):
            self.currFrame.after(1, self.currFrame.clearInput)
            
        self.currFrame = frame

        if hasattr(frame, "onShow"):
            frame.onShow()


            
    def handleEnter(self, event=None):
        if hasattr(self.currFrame, "handleEnter"):
            self.currFrame.handleEnter()
            
    def logout(self):
        for frame in self.frames.values():
            if hasattr(frame, "clearInput"):
                frame.clearInput()
        self.showFrame("WelcomeScreen")
        self.selectedDate = datetime.now().date()