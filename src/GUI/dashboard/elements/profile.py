import customtkinter as ctk
from datetime import datetime
from backend.api.user_submissions import UserSubmissions
from backend.api.db_interactions.get_data import GetData

class Profile(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.getData = GetData()
        self.userSubmissions = UserSubmissions()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        container = ctk.CTkFrame(self)
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(container, text="Profile", font=("Arial", 28, "bold"))
        title.pack(pady=(0, 20))

        # Username
        self.usernameLabel = ctk.CTkLabel(container, text="", font=("Arial", 20))
        self.usernameLabel.pack(pady=10)

        # Date of birth
        self.dobLabel = ctk.CTkLabel(container, text="", font=("Arial", 18))
        self.dobLabel.pack(pady=5)

        dobBtn = ctk.CTkButton(container, text="Edit DOB", command=self.editDOB)
        dobBtn.pack(pady=5)

        # Height
        self.heightLabel = ctk.CTkLabel(container, text="", font=("Arial", 18))
        self.heightLabel.pack(pady=5)

        heightBtn = ctk.CTkButton(container, text="Edit Height", command=self.editHeight)
        heightBtn.pack(pady=5)
        
        goalWeightBtn = ctk.CTkButton(container, text="Edit Goal Weight", command=self.editGoalWeight)
        goalWeightBtn.pack(pady=5)
        
        # Goal Weight
        self.goalWeightLabel = ctk.CTkLabel(container, text="", font=("Arial", 18))
        self.goalWeightLabel.pack(pady=5)

        # Net weight change
        self.netWeightLabel = ctk.CTkLabel(container, text="", font=("Arial", 18))
        self.netWeightLabel.pack(pady=15)

        # Back button
        backBtn = ctk.CTkButton(container, text="< Back", command=lambda: controller.showFrame("Dashboard"))
        backBtn.pack(fill="x", pady=5)

        # Logout button
        logoutBtn = ctk.CTkButton(container, text="Log Out", fg_color="red", hover_color="#aa0000", command=controller.logout)
        logoutBtn.pack(fill="x", pady=10)
        
        # Error
        self.error = ctk.CTkLabel(container, text="", text_color="red")
        self.error.pack(pady=5)

    # Load profile data
    def loadProfile(self):
        # Get user info
        response = self.getData.getDobAndHeight(self.controller.username)
        
        if not response["success"]:
            raise response["message"]

        data = response["data"]
        dob = data["dob"]
        height = data["height"]
        
        self.usernameLabel.configure(text=f"Username: {self.controller.username}")

        self.dobLabel.configure(text=f"Date of Birth: {dob}")
        self.heightLabel.configure(text=f"Height: {height} inches")

        # Weight difference
        weightResp = self.getData.getWeightLogs(self.controller.username)
        if not weightResp["success"]:
            self.netWeightLabel.configure(text=f"N/A")
        weights = [w["weight"] for w in weightResp["data"]]
        diff = weights[-1] - weights[0]
        prefix = "+" if diff >= 0 else ""
        self.netWeightLabel.configure(text=f"Net Weight Change: {prefix}{diff} lbs")
        self.hideError()

    # Edit DOB
    def editDOB(self):
        self.hideError()
        popup = ctk.CTkInputDialog(text="Enter new DOB (YYYY-MM-DD):", title="Edit DOB")
        newDob = popup.get_input()

        # Validate date
        try:
            datetime.strptime(newDob, "%Y-%m-%d")
        except:
            self.showError("Invalid DOB!")
            return

        response = self.userSubmissions.updateDOB(self.controller.username, newDob)
        if not response["success"]:
            raise response["message"]

    # Edit height
    def editHeight(self):
        self.hideError()
        popup = ctk.CTkInputDialog(text="Enter height in inches:", title="Edit Height")
        newHeight = popup.get_input()

        # Error sign
        try:
            newHeight = int(newHeight)
            if newHeight <= 0:
                raise Exception()
        except:
            self.showError("Invalid height!")

        response = self.userSubmissions.insertHeightLog(self.controller.username, int(newHeight), self.controller.selectedDate)
        if not response["success"]:
            raise response["message"]
        
        self.loadProfile()
    
    # Edit goal weight
    def editGoalWeight(self):
        self.hideError()
        popup = ctk.CTkInputDialog(text="Enter your goal weight:", title="Edit Goal Weight")
        newGoalWeight = popup.get_input()

        try:
            newGoalWeight = int(newGoalWeight)
            if newGoalWeight <= 0:
                raise Exception()
        except:
            self.showError("Invalid weight")
            return

        response = self.userSubmissions.updateGoalWeight(self.controller.username, int(newGoalWeight))
        if not response["success"]:
            raise response["message"]

        self.loadProfile()
        
    def showError(self, text):
        self.error.configure(text=text)
        
    def hideError(self):
        self.error.configure(text="")
    
    def onShow(self):
        self.loadProfile()
        