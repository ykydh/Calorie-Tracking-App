import customtkinter as ctk
from datetime import datetime, timedelta
from backend.api.db_interactions.get_data import GetData
from backend.api.user_submissions import UserSubmissions

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

    def previousDay(self):
        self.selectedDate -= timedelta(days=1)
        self.populateInfo()

    def nextDay(self):
        self.selectedDate += timedelta(days=1)
        self.populateInfo()

    def populateInfo(self):
        self.updateDailyLimits()
        self.populateDailyInfo()

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

    def populateDailyInfo(self):
        response = self.getData.getDailyTotals(self.controller.username, self.selectedDate)

        if not response["success"]:
            print(response["message"])
            return
        
        calories = response["data"]["totalCalories"]
        protein = response["data"]["totalProtein"]
        carbs = response["data"]["totalCarbs"]
        fat = response["data"]["totalFat"]
        
        self.calRemaining.configure(text=f"Calories Remaining: {self.dailyCalories - calories}")
        self.proteinRemaining.configure(text=f"Protein Remaining: {self.dailyProtein - protein}")
        self.carbRemaining.configure(text=f"Carbs Remaining: {self.dailyCarbs - carbs}")
        self.fatRemaining.configure(text=f"Fats Remaining: {self.dailyFats - fat}")

    def onShow(self):
        self.populateInfo()