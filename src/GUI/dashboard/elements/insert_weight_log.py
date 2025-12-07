import customtkinter as ctk
from datetime import datetime
from backend.api.user_submissions import UserSubmissions

class InsertWeightLog(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.userSubmissions = UserSubmissions()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Container
        container = ctk.CTkFrame(self)
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(container, text="Log Weight", font=("Arial", 28, "bold"))
        title.pack(pady=(0, 20))

        # Weight entry
        self.weightEntry = ctk.CTkEntry(container, placeholder_text="Enter your weight (lbs)")
        self.weightEntry.pack(fill="x", pady=10)

        # Submit button
        submitBtn = ctk.CTkButton(container, text="Submit", command=self.submitWeight)
        submitBtn.pack(fill="x", pady=(10, 5))

        # Back button
        backBtn = ctk.CTkButton(container, text="< Back", command=lambda: controller.showFrame("Dashboard"))
        backBtn.pack(fill="x", pady=5)

    def submitWeight(self):
        weight_text = self.weightEntry.get()
        if not weight_text.isdigit():
            ctk.CTkLabel(self, text="Please enter a valid number!", text_color="red").pack(pady=5)
            return

        weight = int(weight_text)
        response = self.userSubmissions.insertWeightLog( self.controller.username, weight, self.controller.selectedDate)

        if not response["success"]:
            raise response["message"]

        # Return to dashboard
        self.controller.showFrame("Dashboard")
    def clearInput(self):
        self.weightEntry.delete(0, "end")