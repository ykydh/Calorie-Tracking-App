import customtkinter as ctk
from backend.api.user_submissions import UserSubmissions


class InsertExercise(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.userSubmissions = UserSubmissions()

        self.grid_columnconfigure(0, weight=1)

        # Back button
        backBtn = ctk.CTkButton(self, text="< Back", command=lambda: controller.showFrame("InsertExerciseLog"))
        backBtn.pack(pady=(20, 10), padx=20, anchor="w")

        # Title
        title = ctk.CTkLabel(self, text="Create New Exercise", font=("Arial", 26, "bold"))
        title.pack(pady=10)

        # Error
        self.errorLabel = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 14))
        self.errorLabel.pack(pady=(0, 5))

        # Exercise name entry
        self.nameEntry = ctk.CTkEntry(self, placeholder_text="Exercise Name")
        self.nameEntry.pack(pady=10, fill="x", padx=40)

        # Exercise type buttons
        typeLabel = ctk.CTkLabel(self, text="Exercise Type:", font=("Arial", 16))
        typeLabel.pack(pady=(15, 5))

        self.typeOfExercise = ctk.StringVar(value="cardio") 
        typeFrame = ctk.CTkFrame(self, fg_color="transparent")
        typeFrame.pack(pady=5)

        cardioBtn = ctk.CTkRadioButton(typeFrame, text="Cardio", variable=self.typeOfExercise, value="cardio", command=self.updateTypeFields)
        liftBtn = ctk.CTkRadioButton(typeFrame, text="Lift", variable=self.typeOfExercise, value="lift", command=self.updateTypeFields)

        cardioBtn.grid(row=0, column=0, padx=10)
        liftBtn.grid(row=0, column=1, padx=10)

        # Dynamic fields
        self.typeFieldsFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.typeFieldsFrame.pack(pady=10, fill="x", padx=40)

        # Create blank field holders
        self.calsEntry = None
        self.muscleEntry = None

        # Initialize fields for default type
        self.updateTypeFields()

        # SUBMIT BUTTON
        submitBtn = ctk.CTkButton(self, text="Create Exercise", command=self.submitExercise)
        submitBtn.pack(pady=20, fill="x", padx=40)

    # Dynamically switch input fields based on type
    def updateTypeFields(self):
        self.errorLabel.configure(text="")

        for widget in self.typeFieldsFrame.winfo_children():
            widget.destroy()

        if self.typeOfExercise.get() == "cardio":
            label = ctk.CTkLabel(self.typeFieldsFrame, text="Calories per Minute:")
            label.pack(anchor="w", pady=(0, 5))
            self.calsEntry = ctk.CTkEntry(self.typeFieldsFrame, placeholder_text="e.g., 12.5")
            self.calsEntry.pack(fill="x")

        else:  # Lift
            label = ctk.CTkLabel(self.typeFieldsFrame, text="Muscles Worked:")
            label.pack(anchor="w", pady=(0, 5))
            self.muscleEntry = ctk.CTkEntry(self.typeFieldsFrame, placeholder_text="e.g., Chest, Triceps")
            self.muscleEntry.pack(fill="x")

    # Submit to database
    def submitExercise(self):
        self.errorLabel.configure(text="")

        name = self.nameEntry.get().strip()
        typeVal = self.typeOfExercise.get()

        if not name:
            self.errorLabel.configure(text="Missing name")
            return

        if typeVal == "cardio":
            cbpm = self.calsEntry.get().strip()
            if not cbpm:
                self.errorLabel.configure(text="Missing calories/min")
                return

            response = self.userSubmissions.insertExercise(name, "c", float(cbpm), None)

        else:  # Lift
            muscles = self.muscleEntry.get().strip()
            if not muscles:
                self.errorLabel.configure(text="Missing muscles worked")
                return

            response = self.userSubmissions.insertExercise(name, "l", None, muscles)

        if not response["success"]:
            raise response["message"]

        # Return to previous screen
        self.controller.showFrame("InsertExerciseLog")
    
    def clearInput(self):
        self.nameEntry.delete(0, "end")
        if not self.calsEntry is None:
            self.calsEntry.delete(0, "end")
        if not self.muscleEntry is None:
            self.muscleEntry.delete(0, "end")