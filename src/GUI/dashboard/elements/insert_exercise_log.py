import customtkinter as ctk
from backend.api.user_submissions import UserSubmissions
from backend.api.db_interactions.get_data import GetData
from backend.objects.exercise.cardio import Cardio
from backend.objects.exercise.lift import Lift

class InsertExerciseLog(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.userSubmissions = UserSubmissions()
        self.getData = GetData()
        self.selectedExercise = None
        
        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left pane for searching
        left = ctk.CTkFrame(self)
        left.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        backBtn = ctk.CTkButton(left, text="< Back", command=lambda: controller.showFrame("Dashboard"))
        backBtn.pack(fill="x", pady=(0, 15))

        title = ctk.CTkLabel(left, text="Log Exercise", font=("Arial", 24, "bold"))
        title.pack(pady=(0, 20))

        self.nameEntry = ctk.CTkEntry(left, placeholder_text="Exercise Name")
        self.nameEntry.pack(fill="x", pady=10)

        searchBtn = ctk.CTkButton(left, text="Search", command=self.searchExercises)
        searchBtn.pack(expand=True, fill="x", padx=(0, 5))

        # Results
        resultsFrame = ctk.CTkFrame(left)
        resultsFrame.pack(fill="both", expand=True, pady=20)

        resultsTitle = ctk.CTkLabel(resultsFrame, text="Results", font=("Arial", 20, "bold"))
        resultsTitle.pack(pady=(0, 10))

        self.resultsBox = ctk.CTkScrollableFrame(resultsFrame, width=300)
        self.resultsBox.pack(expand=True, fill="both")

        createExerciseBtn = ctk.CTkButton(
            left,
            text="Create New Exercise",
            command=lambda: controller.showFrame("InsertExercise")
        )
        createExerciseBtn.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Right panel
        self.right = ctk.CTkFrame(self)
        self.right.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.rightTitle = ctk.CTkLabel(self.right, text="Select an exercise…", font=("Arial", 24))
        self.rightTitle.pack(pady=10)

        self.infoFrame = ctk.CTkFrame(self.right, fg_color="transparent")
        self.infoFrame.pack(fill="x", pady=10)

        # Minutes performed
        self.minutesEntry = ctk.CTkEntry(self.right, placeholder_text="Minutes performed")
        self.submitBtn = ctk.CTkButton(self.right, text="Submit", command=self.submitExerciseLog)

    # Searching
    def searchExercises(self):
        name = self.nameEntry.get()

        response = self.getData.getExercisesLike(name)

        # Clear previous results
        for w in self.resultsBox.winfo_children():
            w.destroy()

        if not response["success"]:
            raise response["message"]

        data = response["data"]

        if not data:
            ctk.CTkLabel(self.resultsBox, text="No matching exercises found.").pack()
            return

        for exerciseMap in data:
            if exerciseMap["type"] == "c":
                exercise = Cardio(
                    exerciseMap["exerciseID"],
                    exerciseMap["name"],
                    exerciseMap["exerciseID"],
                    exerciseMap["caloriesPerMinute"],
                    None
                )
            else:
                exercise = Lift(
                    exerciseMap["exerciseID"],
                    exerciseMap["name"],
                    exerciseMap["exerciseID"],
                    exerciseMap["musclesWorked"],
                    None
                )

            btn = ctk.CTkButton(
                self.resultsBox,
                text=f"{exercise.name}",
                command=lambda e=exercise: self.selectExercise(e),
                fg_color="#333333",
                hover_color="#444444"
            )
            btn.pack(fill="x", pady=5)

    # Selecting an exercise
    def selectExercise(self, exercise):
        self.selectedExercise = exercise

        for w in self.infoFrame.winfo_children():
            w.destroy()

        self.rightTitle.configure(text=f"{exercise.name}")

        if isinstance(exercise, Cardio):
            ctk.CTkLabel(
                self.infoFrame,
                text=f"Calories/min: {exercise.cbpm:.2f}",
                font=("Arial", 16)
            ).pack(anchor="w")
        else:
            ctk.CTkLabel(
                self.infoFrame,
                text=f"Muscles worked: {exercise.musclesWorked}",
                font=("Arial", 16)
            ).pack(anchor="w")

        self.minutesEntry.pack(pady=10)
        self.submitBtn.pack(pady=5)

    # Submitting exercise log
    def submitExerciseLog(self):
        if not self.selectedExercise:
            return

        minutes = int(self.minutesEntry.get())
        exerciseID = self.selectedExercise.exerciseID

        response = self.userSubmissions.insertExerciseLog(
            self.controller.username,
            exerciseID,
            minutes,
            self.controller.selectedDate
        )

        if not response["success"]:
            raise response["message"]

        self.controller.showFrame("Dashboard")
        
    def clearInput(self):
        self.nameEntry.delete(0, "end")
        self.minutesEntry.delete(0, "end")