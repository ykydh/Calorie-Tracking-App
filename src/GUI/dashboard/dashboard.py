import customtkinter as ctk
from datetime import datetime, timedelta
from backend.api.db_interactions.get_data import GetData
from backend.api.user_submissions import UserSubmissions
from GUI.dashboard.elements.insert_exercise_log import InsertExerciseLog
from GUI.dashboard.elements.insert_exercise import InsertExercise
from GUI.dashboard.elements.insert_food_log import InsertFoodLog
from GUI.dashboard.elements.insert_food import InsertFood
from GUI.dashboard.elements.insert_weight_log import InsertWeightLog
from GUI.dashboard.elements.profile import Profile

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.selectedDate = datetime.now().date()
        self.getData = GetData()
        self.userSubmissions = UserSubmissions()
        self.dailyCalories = None
        self.dailyProtein = None
        self.dailyCarbs = None
        self.dailyFats = None

        # Setup framework
        self.grid_rowconfigure(0, weight=1)   # full height for left column
        self.grid_columnconfigure(0, weight=1) # left (Food Log)
        self.grid_columnconfigure(1, weight=2) # right side (Exercise + Macros + Graph)

        # Food log
        foodFrame = ctk.CTkFrame(self, corner_radius=15)
        foodFrame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        foodFrame.grid_rowconfigure(0, weight=1)
        foodFrame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(foodFrame, text="Food Log", font=("Arial", 28)).pack(pady=10)
        self.foodList = ctk.CTkTextbox(foodFrame)
        self.foodList.pack(expand=True, fill="both", padx=10, pady=10)

        foodFrame.bind("<Button-1>", lambda e: controller.showFoodScreen())
        self.foodList.bind("<Button-1>", lambda e: controller.showFoodScreen())

        # Container for exercise & weight log, as well as daily nutrition
        rightFrame = ctk.CTkFrame(self, fg_color="transparent")
        rightFrame.grid(row=0, column=1, sticky="nsew", padx=(10,20), pady=20)
        rightFrame.grid_rowconfigure(0, weight=0)  
        rightFrame.grid_rowconfigure(1, weight=1)
        rightFrame.grid_rowconfigure(2, weight=1)  
        rightFrame.grid_columnconfigure(0, weight=1)

        # Toolbar
        toolbar = ctk.CTkFrame(rightFrame, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="nsew", pady=20)
        toolbar.grid_columnconfigure(0, weight=1)
        toolbar.grid_columnconfigure(1, weight=0)
        toolbar.grid_columnconfigure(2, weight=0)
        toolbar.grid_columnconfigure(3, weight=0)
        toolbar.grid_columnconfigure(4, weight=1)

        # Title
        title = ctk.CTkLabel(toolbar, text="Macro Tracker", font=("Arial", 32))
        title.grid(row=0, column=0, sticky="nw")

        # Date selecter
        backDateBtn = ctk.CTkButton(toolbar, text="<", width=30, height=30,command=None)
        backDateBtn.grid(row=0, column=1, sticky="e")

        dateLabel = ctk.CTkLabel(toolbar, text=self.selectedDate, font=("Arial", 18))
        dateLabel.grid(row=0, column=2, sticky="nsew", padx = 10)

        nextDateBtn = ctk.CTkButton(toolbar, text=">", width=30, height=30,command=None)
        nextDateBtn.grid(row=0, column=3, sticky="w")

        # Profile Button
        profileBtn = ctk.CTkButton(toolbar, text="👤", width=50, height=50, command=None)
        profileBtn.grid(row=0, column=4, sticky="ne")

        # Container for top half of right side container
        topRight = ctk.CTkFrame(rightFrame, fg_color="transparent")
        topRight.grid(row=1, column=0, sticky="nsew")
        topRight.grid_rowconfigure(0, weight=1)
        topRight.grid_columnconfigure(0, weight=1)
        topRight.grid_columnconfigure(1, weight=1)
        
        # Exercise log
        exerciseFrame = ctk.CTkFrame(topRight, corner_radius=15)
        exerciseFrame.grid(row=0, column=0, sticky="nsew", padx=(0,10))
        exerciseFrame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(exerciseFrame, text="Exercise Log", font=("Arial", 28)).pack(pady=10)
        self.exerciseList = ctk.CTkTextbox(exerciseFrame, height=200)
        self.exerciseList.pack(expand=True, fill="both", padx=10, pady=10)

        exerciseFrame.bind("<Button-1>", lambda e: controller.showExerciseScreen())
        self.exerciseList.bind("<Button-1>", lambda e: controller.showExerciseScreen())

        # Daily nutrition
        macrosFrame = ctk.CTkFrame(topRight, corner_radius=15)
        macrosFrame.grid(row=0, column=1, sticky="nsew", padx=(10,0))

        ctk.CTkLabel(macrosFrame, text="Today's Nutrition", font=("Arial", 28)).pack(pady=10)

        self.calRemaining = ctk.CTkLabel(macrosFrame, text="")
        self.calRemaining.pack()
        self.calBar = ctk.CTkProgressBar(macrosFrame, width=250)
        self.calBar.pack(pady=5)

        self.proteinRemaining = ctk.CTkLabel(macrosFrame, text="")
        self.proteinRemaining.pack()
        self.proteinBar = ctk.CTkProgressBar(macrosFrame, width=250)
        self.proteinBar.pack(pady=5)

        self.carbRemaining = ctk.CTkLabel(macrosFrame, text="")
        self.carbRemaining.pack()
        self.carbsBar = ctk.CTkProgressBar(macrosFrame, width=250)
        self.carbsBar.pack(pady=5)

        self.fatRemaining = ctk.CTkLabel(macrosFrame, text="")
        self.fatRemaining.pack()
        self.fatsBar = ctk.CTkProgressBar(macrosFrame, width=250)
        self.fatsBar.pack(pady=5)

        # Weight graph
        bottomRight = ctk.CTkFrame(rightFrame, corner_radius=15)
        bottomRight.grid(row=2, column=0, sticky="nsew", pady=(10,0))
        bottomRight.grid_rowconfigure(0, weight=1)
        bottomRight.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(bottomRight, text="Weight Progress", font=("Arial", 28)).pack(pady=10)

        self.weightGraph = ctk.CTkFrame(bottomRight, height=250, fg_color="#1e1e1e")
        self.weightGraph.pack(expand=True, fill="both", padx=10, pady=10)

        self.weightGraph.bind("<Button-1>", lambda e: controller.showWeightScreen())

    def addFoodLogToList(self, foodLog):
        # Outer frame for each food log
        logFrame = ctk.CTkFrame(self.foodListCanvas, corner_radius=10, fg_color="#2e2e2e")
        logFrame.pack(fill="x", pady=5, padx=5)

        # Left part: labels
        labelsFrame = ctk.CTkFrame(logFrame, fg_color="transparent")
        labelsFrame.pack(side="left", expand=True, fill="both", padx=5, pady=5)

        brandLabel = ctk.CTkLabel(labelsFrame, text=foodLog.brand, font=("Arial", 12))
        brandLabel.pack(anchor="w")

        nameLabel = ctk.CTkLabel(labelsFrame, text=foodLog.name, font=("Arial", 20))
        nameLabel.pack(anchor="w")

        
        infoLabel = ctk.CTkLabel(
            labelsFrame, 
            text=f"{foodLog.weight}g | {foodLog.calories:.2f}cal | {foodLog.protein:.2f}g protein | {foodLog.carbs:.2f}g carbs | {foodLog.fat:.2f}g fat", 
            font=("Arial", 10)
        )
        infoLabel.pack(anchor="w")

        # Right part: buttons
        btnFrame = ctk.CTkFrame(logFrame, fg_color="transparent")
        btnFrame.pack(side="right", padx=5, pady=5)

        editBtn = ctk.CTkButton(btnFrame, text="✏️", width=30, height=30, command=lambda fl=foodLog: self.editFoodLog(fl))
        editBtn.pack(pady=2)

        deleteBtn = ctk.CTkButton(btnFrame, text="🗑️", width=30, height=30, command=lambda fl=foodLog: self.deleteFoodLog(fl))
        deleteBtn.pack(pady=2)

    def previousDay(self):
        self.selectedDate -= timedelta(days=1)
        self.populateInfo()

    def nextDay(self):
        self.selectedDate += timedelta(days=1)
        self.populateInfo()

    def populateInfo(self):
        self.updateDailyLimits()
        self.populateDailyInfo()
        self.populateFoodInfo()

    def updateDailyLimits(self):
        response = self.userSubmissions.calculateInfoAtTime(self.controller.username, self.selectedDate)
        if not response["success"]:
            print(response["message"])
            return
        
        data = response["data"]
        self.dailyCalories = data["calories"]
        self.dailyProtein = data["protein"]
        self.dailyCarbs = data["carbs"]
        self.dailyFats = data["fat"]
        
    def populateFoodInfo(self):
        for widget in self.foodList.winfo_children():
            widget.destroy()

        self.foodListCanvas = ctk.CTkScrollableFrame(self.foodList)
        self.foodListCanvas.pack(expand=True, fill="both", padx=10, pady=10)
        
        response = self.getData.getFoodLogsWithInfo(self.controller.username, self.selectedDate)
        if not response["success"]:
            print(response["message"])
            return
        
        data = response["data"]
        for foodLog in data:
            self.addFoodLog(foodLog)
            
    

    def populateDailyInfo(self):
        response = self.getData.getDailyTotals(self.controller.username, self.selectedDate)

        if not response["success"]:
            print(response["message"])
            return
        
        caloriesRemaining = self.dailyCalories - response["data"]["totalCalories"]
        proteinRemaining = self.dailyProtein - response["data"]["totalProtein"]
        carbsRemaining = self.dailyCarbs - response["data"]["totalCarbs"]
        fatRemaining = self.dailyFats - response["data"]["totalFat"]
        
        self.calRemaining.configure(text=f"Calories Remaining: {(caloriesRemaining):.2f}")
        self.proteinRemaining.configure(text=f"Protein Remaining: {(proteinRemaining):.2f}")
        self.carbRemaining.configure(text=f"Carbs Remaining: {(carbsRemaining):.2f}")
        self.fatRemaining.configure(text=f"Fats Remaining: {(fatRemaining):.2f}")
        
        self.calBar.set(1 - (caloriesRemaining / self.dailyCalories))
        self.proteinBar.set(1 - (proteinRemaining / self.dailyProtein))
        self.carbsBar.set(1 - (carbsRemaining / self.dailyCarbs))
        self.fatsBar.set(1 - (fatRemaining / self.dailyFats))

    def onShow(self):
        self.populateInfo()