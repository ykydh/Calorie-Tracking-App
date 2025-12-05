import customtkinter as ctk

import customtkinter as ctk
# from Callers.sign_up_caller import SignUpCaller

class Biometrics(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        # self.signUpCaller = SignUpCaller()
        
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

        # Height entry
        self.heightEntry = ctk.CTkEntry(content, width=300, height=40, placeholder_text="Height (inches)")
        self.heightEntry.pack(pady=10)

        # Age entry
        self.ageEntry = ctk.CTkEntry(content, width=300, height=40, placeholder_text="Age")
        self.ageEntry.pack(pady=10)

        # Error
        self.errorLabel = ctk.CTkLabel(content, text="", text_color="red")
        self.errorLabel.pack(pady=5)
        self.errorLabel.pack_forget()

        ctk.CTkButton(content, width=300, height=40, text="Biometrics", command=self.handleBiometrics).pack(pady=20)

    def handleBiometrics(self):
        self.hideError()
        
        try:
            weight = float(self.weightEntry.get())
        except:
            self.showError("Invalid weight")
        
        try:
            height = float(self.heightEntry.get())
        except:
            self.showError("Invalid height")
            
        try:
            age = int(self.ageEntry.get())
        except:
            self.showError("Invalid age")
            
        

    def showError(self, message):
        self.errorLabel.configure(text=message)
        self.errorLabel.pack(pady=5)

    def hideError(self):
        self.errorLabel.pack_forget()
        
    def handleEnter(self):
        self.handleSignUp()