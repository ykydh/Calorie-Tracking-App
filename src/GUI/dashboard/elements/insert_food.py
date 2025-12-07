import customtkinter as ctk
from backend.api.user_submissions import UserSubmissions

class InsertFood(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.userSubmissions = UserSubmissions()  # assumes this handles DB insert

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Container frame
        container = ctk.CTkFrame(self)
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(container, text="Add New Food", font=("Arial", 28, "bold"))
        title.pack(pady=(0, 20))

        # Food name
        self.nameEntry = ctk.CTkEntry(container, placeholder_text="Food Name")
        self.nameEntry.pack(fill="x", pady=5)

        # Brand
        self.brandEntry = ctk.CTkEntry(container, placeholder_text="Brand")
        self.brandEntry.pack(fill="x", pady=5)

        # Serving size in grams
        self.servingEntry = ctk.CTkEntry(container, placeholder_text="Serving Size (g)")
        self.servingEntry.pack(fill="x", pady=5)

        # Calories per gram
        self.caloriesEntry = ctk.CTkEntry(container, placeholder_text="Calories per gram")
        self.caloriesEntry.pack(fill="x", pady=5)

        # Protein per gram
        self.proteinEntry = ctk.CTkEntry(container, placeholder_text="Protein per gram")
        self.proteinEntry.pack(fill="x", pady=5)

        # Carbs per gram
        self.carbsEntry = ctk.CTkEntry(container, placeholder_text="Carbs per gram")
        self.carbsEntry.pack(fill="x", pady=5)

        # Fat per gram
        self.fatEntry = ctk.CTkEntry(container, placeholder_text="Fat per gram")
        self.fatEntry.pack(fill="x", pady=5)

        # Submit button
        submitBtn = ctk.CTkButton(container, text="Submit", command=self.submitFood)
        submitBtn.pack(fill="x", pady=(15, 5))

        # Back button
        backBtn = ctk.CTkButton(container, text="< Back", command=lambda: controller.showFrame("InsertFoodLog"))
        backBtn.pack(fill="x", pady=5)

    def submitFood(self):
        try:
            name = self.nameEntry.get().strip()
            brand = self.brandEntry.get().strip()
            serving = float(self.servingEntry.get())
            calories = float(self.caloriesEntry.get())
            protein = float(self.proteinEntry.get())
            carbs = float(self.carbsEntry.get())
            fat = float(self.fatEntry.get())

            if not name or not brand or not serving:
                raise ValueError("Food name, brand, and serving cannot be empty.")
            if calories is None: calories = 0
            if protein is None: protein = 0
            if carbs is None: carbs = 0
            if fat is None: fat = 0
            
            unitCals = calories / serving
            unitProtien = protein / serving
            unitCarbs = carbs / serving
            unitFat = fat / serving

            response = self.userSubmissions.insertFood(name, brand, unitCals, unitProtien, unitCarbs, unitFat)

            if not response["success"]:
                raise ValueError(response.get("message", "Failed to insert food."))

            # Return to InsertFoodLog
            self.controller.showFrame("InsertFoodLog")

        except:
            ctk.CTkLabel(self, text="Invalid input.", text_color="red").pack(pady=5)
            
    def clearInput(self):
        self.fatEntry.delete(0, "end")
        self.nameEntry.delete(0, "end")
        self.brandEntry.delete(0, "end")
        self.carbsEntry.delete(0, "end")
        self.proteinEntry.delete(0, "end")
        self.servingEntry.delete(0, "end")
        self.caloriesEntry.delete(0, "end")