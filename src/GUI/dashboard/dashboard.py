import customtkinter as ctk
import matplotlib
matplotlib.use("Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from datetime import datetime, timedelta
from backend.api.db_interactions.get_data import GetData
from backend.api.user_submissions import UserSubmissions

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

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

        # Header for food log
        foodHeader = ctk.CTkFrame(foodFrame, fg_color="transparent")
        foodHeader.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(foodHeader, text="Food Log", font=("Arial", 28)).pack(side="left")

        addFoodBtn = ctk.CTkButton(
            foodHeader, text="+", width=40, height=40,
            command=self.openInsertFoodLog
        )
        addFoodBtn.pack(side="right")

        self.foodList = ctk.CTkScrollableFrame(foodFrame)
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

        # Date select
        backDateBtn = ctk.CTkButton(toolbar, text="<", width=30, height=30,command=self.previousDay)
        backDateBtn.grid(row=0, column=1, sticky="e")

        self.dateLabel = ctk.CTkLabel(toolbar, font=("Arial", 18))
        self.dateLabel.grid(row=0, column=2, sticky="nsew", padx = 10)

        nextDateBtn = ctk.CTkButton(toolbar, text=">", width=30, height=30,command=self.nextDay)
        nextDateBtn.grid(row=0, column=3, sticky="w")

        # Profile Button
        profileBtn = ctk.CTkButton(toolbar, text="👤", width=50, height=50, command=self.showProfile)
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

        # Exercise header
        exerciseHeader = ctk.CTkFrame(exerciseFrame, fg_color="transparent")
        exerciseHeader.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(exerciseHeader, text="Exercise Log", font=("Arial", 28)).pack(side="left")

        addExerciseBtn = ctk.CTkButton(
            exerciseHeader, text="+", width=40, height=40,
            command=self.openInsertExerciseLog
        )
        addExerciseBtn.pack(side="right")
        self.exerciseList = ctk.CTkScrollableFrame(exerciseFrame)
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

        # Weight header
        weightHeader = ctk.CTkFrame(bottomRight, fg_color="transparent")
        weightHeader.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(weightHeader, text="Weight Progress", font=("Arial", 28)).pack(side="left")

        addWeightBtn = ctk.CTkButton(
            weightHeader, text="+", width=40, height=40,
            command=self.openInsertWeightLog
        )
        addWeightBtn.pack(side="right")

        self.weightGraph = ctk.CTkFrame(bottomRight, height=250, fg_color="#1e1e1e")
        self.weightGraph.pack(expand=True, fill="both", padx=10, pady=10)

        self.weightGraph.bind("<Button-1>", lambda e: controller.showWeightScreen())

    def addFoodLogToList(self, foodLog):
        # Outer frame for each food log
        logFrame = ctk.CTkFrame(self.foodList, corner_radius=10, fg_color="#2e2e2e")
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
        self.controller.selectedDate -= timedelta(days=1)
        self.populateInfo()

    def nextDay(self):
        self.controller.selectedDate += timedelta(days=1)
        self.populateInfo()

    def populateInfo(self):
        try:
            self.updateDailyLimits()
            self.populateDailyInfo()
            self.populateFoodInfo()
            self.populateExerciseInfo()
            self.updateWeightGraph()
        except:
            self.controller.selectedDate += timedelta(days=1)
            return 
        self.dateLabel.configure(text=self.controller.selectedDate)

    def updateDailyLimits(self):
        response = self.userSubmissions.calculateInfoAtTime(self.controller.username, self.controller.selectedDate)
        if not response["success"]:
            raise response
        
        data = response["data"]
        self.dailyCalories = data["calories"]
        self.dailyProtein = data["protein"]
        self.dailyCarbs = data["carbs"]
        self.dailyFats = data["fat"]
        
    def populateFoodInfo(self):
        for widget in self.foodList.winfo_children():
            widget.destroy()
        
        response = self.getData.getFoodLogsWithInfo(self.controller.username, self.controller.selectedDate)
        if not response["success"]:
            raise response["message"]
        
        data = response["data"]
        
        for foodLog in data:
            self.addFoodLogToList(foodLog)

    def populateDailyInfo(self):
        response = self.getData.getDailyTotals(self.controller.username, self.controller.selectedDate)

        if not response["success"]:
            raise(response["message"])
        
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

    def populateExerciseInfo(self):
        # Clear existing logs
        for widget in self.exerciseList.winfo_children():
            widget.destroy()

        # Get logs from DB
        response = self.getData.getExerciseLogs(self.controller.username, self.controller.selectedDate)

        if not response["success"]:
            raise response["message"]

        data = response["data"]

        if not data:
            ctk.CTkLabel(self.exerciseList, text="No exercises logged.").pack(pady=5)
            return

        # Display logs
        for log in data:
            self.addExerciseLogToList(log)

    def addExerciseLogToList(self, log):
        # Container
        logFrame = ctk.CTkFrame(self.exerciseList, corner_radius=10, fg_color="#2e2e2e")
        logFrame.pack(fill="x", pady=5, padx=5)

        # Left text
        textFrame = ctk.CTkFrame(logFrame, fg_color="transparent")
        textFrame.pack(side="left", expand=True, fill="both", padx=5, pady=5)

        ctk.CTkLabel(textFrame, text=log.name, font=("Arial", 18)).pack(anchor="w")
        ctk.CTkLabel(textFrame, text=f"{log.minutes}min | {log.getInfo()}", font=("Arial", 12)).pack(anchor="w")

        # Right button area
        btnFrame = ctk.CTkFrame(logFrame, fg_color="transparent")
        btnFrame.pack(side="right", padx=5, pady=5)

        editBtn = ctk.CTkButton(btnFrame, text="✏️", width=30, height=30, command=lambda l=log: self.editExerciseLog(l))
        editBtn.pack(pady=2)

        deleteBtn = ctk.CTkButton(btnFrame, text="🗑️", width=30, height=30, command=lambda l=log: self.deleteExerciseLog(l))
        deleteBtn.pack(pady=2)

    def updateWeightGraph(self):
        # Clear existing graph
        for widget in self.weightGraph.winfo_children():
            widget.destroy()

        # Get weight logs
        response = self.getData.getWeightLogs(self.controller.username)

        if not response["success"]:
            ctk.CTkLabel(self.weightGraph, text="Unable to load weight data.").pack(pady=10)
            return

        data = response["data"]

        # If no logs
        if len(data) == 0:
            ctk.CTkLabel(self.weightGraph, text="No weight entries yet.").pack(pady=10)
            return
        
        dates = []
        weights = []
        for log in data:
            if (datetime.strptime(log["date"], "%Y-%m-%d").date() >= datetime.now().date() - timedelta(days=30)):
                dates.append(log["date"])
                weights.append(log["weight"])

        # Matplotlib figure
        fig = Figure(figsize=(5, 2.2), dpi=100)
        ax = fig.add_subplot(111)

        # Plot
        ax.plot(dates, weights, marker="o", linewidth=2)
        ax.set_title("Last 30 Days")
        ax.set_ylabel("Weight (lbs)")
        ax.tick_params(axis="x", rotation=30)
        ax.grid(True, alpha=0.3)

        # Embed inside CTk frame
        canvas = FigureCanvasTkAgg(fig, master=self.weightGraph)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")


    def onShow(self):
        self.populateInfo()

    def openInsertFoodLog(self):
        self.controller.showFrame("InsertFoodLog")

    def openInsertExerciseLog(self):
        self.controller.showFrame("InsertExerciseLog")

    def openInsertWeightLog(self):
        self.controller.showFrame("InsertWeightLog")
        
    def deleteFoodLog(self, log):
        response = self.userSubmissions.deleteFoodLog(log.logID)
        if response["success"]:
            self.populateInfo()
        else:
            raise(response["message"])
        
    def deleteExerciseLog(self, log):
        response = self.userSubmissions.deleteExerciseLog(log.logID)
        if response["success"]:
            self.populateInfo()
        else:
            raise(response["message"])
        
    def showProfile(self):
        self.controller.showFrame("Profile")
        
    def editFoodLog(self, log):
        # Ask for new weight in grams
        popup = ctk.CTkInputDialog(text=f"Edit weight for {log.name} (current: {log.weight}g):", title="Edit Food Log")
        newWeight = popup.get_input()

        # Cancelled
        if newWeight is None:
            return

        # Validate
        try:
            newWeight = float(newWeight)
            if newWeight <= 0:
                raise Exception()
        except:
            ctk.CTkLabel(self.foodList, text="Invalid weight!", text_color="red").pack()
            return

        # Update log
        response = self.userSubmissions.updateFoodLog(log.logID, newWeight)

        if not response["success"]:
            raise Exception(response["message"])

        self.populateInfo()
        
    def editExerciseLog(self, log):
        # Ask for new time
        popup = ctk.CTkInputDialog(text=f"Edit time for {log.name} (current: {log.minutes}min):", title="Edit Exercise Log")
        newTime = popup.get_input()

        # Cancelled
        if newTime is None:
            return

        # Validate
        try:
            newTime = float(newTime)
            if newTime <= 0:
                raise Exception()
        except:
            ctk.CTkLabel(self.exerciseList, text="Invalid time!", text_color="red").pack()
            return

        # Update log
        response = self.userSubmissions.updateExerciseLog(log.logID, newTime)

        if not response["success"]:
            raise Exception(response["message"])

        self.populateInfo()

