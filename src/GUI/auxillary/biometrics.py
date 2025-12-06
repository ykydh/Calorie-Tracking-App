import customtkinter as ctk

from backend.api.user_submissions import UserSubmissions

class Biometrics(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.userSubmissions = UserSubmissions()
        
        # Configure grid to center contents and scale with window
        self.grid_rowconfigure(0, weight=1)   # top spacer
        self.grid_rowconfigure(1, weight=0)   # content row
        self.grid_rowconfigure(2, weight=1)   # bottom spacer
        self.grid_columnconfigure(0, weight=1)  # left spacer
        self.grid_columnconfigure(1, weight=0)  # content column
        self.grid_columnconfigure(2, weight=1)  # right spacer

        # Create a container frame for the centered widgets
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=1)

        # Elements added to center 
        ctk.CTkLabel(content, text="Biometrics", font=("Arial", 56)).pack(pady=30)

        # Weight entry
        self.weightEntry = ctk.CTkEntry(content, width=300, height=40, placeholder_text="Weight (lbs.)")
        self.weightEntry.pack(pady=10)

        # Goal weight
        self.goalWeightEntry = ctk.CTkEntry(content, width=300, height=40, placeholder_text="Goal Weight (lbs.)")
        self.goalWeightEntry.pack(pady=10)

        # Height entry
        self.heightEntry = ctk.CTkEntry(content, width=300, height=40, placeholder_text="Height (inches)")
        self.heightEntry.pack(pady=10)

        # Goal Date entry frame
        goalDateEntryFrame = ctk.CTkFrame(content, width=300, height=40)
        goalDateEntryFrame.pack(pady=10, fill="x")
        goalDateEntryFrame.grid_rowconfigure(0, weight=1)
        goalDateEntryFrame.grid_rowconfigure(1, weight=1)
        goalDateEntryFrame.grid_columnconfigure(0, weight=1)
        goalDateEntryFrame.grid_columnconfigure(1, weight=1)
        goalDateEntryFrame.grid_columnconfigure(2, weight=1)

        # DOB label
        ctk.CTkLabel(goalDateEntryFrame, text="Goal date", font=("Arial", 18)).grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        # Year entry
        self.goalYearEntry = ctk.CTkEntry(goalDateEntryFrame, placeholder_text="Year")
        self.goalYearEntry.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

        # Month entry
        self.goalMonthEntry = ctk.CTkEntry(goalDateEntryFrame, placeholder_text="Month")
        self.goalMonthEntry.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        # Day entry
        self.goalDayEntry = ctk.CTkEntry(goalDateEntryFrame, placeholder_text="Day")
        self.goalDayEntry.grid(row=1, column=2, padx=5, pady=10, sticky="ew")

        # DOB entry frame
        ageEntryFrame = ctk.CTkFrame(content, width=300, height=40)
        ageEntryFrame.pack(pady=10, fill="x")
        ageEntryFrame.grid_rowconfigure(0, weight=1)
        ageEntryFrame.grid_rowconfigure(1, weight=1)
        ageEntryFrame.grid_columnconfigure(0, weight=1)
        ageEntryFrame.grid_columnconfigure(1, weight=1)
        ageEntryFrame.grid_columnconfigure(2, weight=1)

        # DOB label
        ctk.CTkLabel(ageEntryFrame, text="Date of brith", font=("Arial", 18)).grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        # Year entry
        self.yearEntry = ctk.CTkEntry(ageEntryFrame, placeholder_text="Year")
        self.yearEntry.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

        # Month entry
        self.monthEntry = ctk.CTkEntry(ageEntryFrame, placeholder_text="Month")
        self.monthEntry.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        # Day entry
        self.dayEntry = ctk.CTkEntry(ageEntryFrame, placeholder_text="Day")
        self.dayEntry.grid(row=1, column=2, padx=5, pady=10, sticky="ew")

        # Error
        self.errorLabel = ctk.CTkLabel(content, text="", text_color="red")
        self.errorLabel.pack(pady=5)
        self.errorLabel.pack_forget()

        ctk.CTkButton(content, width=300, height=40, text="Submit", command=self.handleBiometrics).pack(pady=20)

    def handleBiometrics(self):
        self.hideError()

        val = self.weightEntry.get()
        if len(val):
            response = self.userSubmissions.addWeightLog(self.controller.username, val)
            if not response["success"]:
                self.showError("Invalid weight")
                return
        else:
            self.showError("Must enter weight")
            return

        val = self.goalWeightEntry.get()
        if len(val):
            response = self.userSubmissions.updateGoalWeight(self.controller.username, val)
            if not response["success"]:
                self.showError("Invalid goal weight")
                return
        else:
            self.showError("Must enter goal weight")
            return

        val = self.heightEntry.get()
        if len(val):
            response = self.userSubmissions.addHeightLog(self.controller.username, val)
            if not response["success"]:
                self.showError("Invalid height")
                return
        else:
            self.showError("Must enter height")
            return
        
        val = self.goalYearEntry.get() + '-' + self.goalMonthEntry.get() + '-' + self.goalDayEntry.get()
        if len(val):
            response = self.userSubmissions.updateGoalDate(self.controller.username, val)
            if not response["success"]:
                self.showError(response["message"])
                return
        else:
            self.showError("Must enter DOB")
            return
        
        val = self.yearEntry.get() + '-' + self.monthEntry.get() + '-' + self.dayEntry.get()
        if len(val):
            response = self.userSubmissions.changeDOB(self.controller.username, val)
            if not response["success"]:
                self.showError(response["message"])
                return
        else:
            self.showError("Must enter DOB")
            return
        
        self.controller.showFrame("Dashboard")
            
        

    def showError(self, message):
        self.errorLabel.configure(text=message)
        self.errorLabel.pack(pady=5)

    def hideError(self):
        self.errorLabel.pack_forget()
        
    def handleEnter(self):
        self.handleBiometrics()