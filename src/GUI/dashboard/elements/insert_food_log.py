import customtkinter as ctk
from backend.api.user_submissions import UserSubmissions
from backend.objects.food import Food
from backend.api.db_interactions.get_data import GetData

class InsertFoodLog(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.userSubmissions = UserSubmissions()
        self.getData = GetData()
        
        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left pane for searching
        left = ctk.CTkFrame(self)
        left.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        backBtn = ctk.CTkButton(left, text="< Back", command=lambda: controller.showFrame("Dashboard"))
        backBtn.pack(fill="x", pady=(0, 15))

        title = ctk.CTkLabel(left, text="Log Food", font=("Arial", 24, "bold"))
        title.pack(pady=(0, 20))

        self.brandEntry = ctk.CTkEntry(left, placeholder_text="Brand")
        self.brandEntry.pack(fill="x", pady=10)

        self.nameEntry = ctk.CTkEntry(left, placeholder_text="Food Name")
        self.nameEntry.pack(fill="x", pady=10)

        # Button to search
        searchBtn = ctk.CTkButton(left, text="Search", command=self.searchFoods)
        searchBtn.pack(expand=True, fill="x", padx=(0, 5))

        # Results
        resultsFrame = ctk.CTkFrame(left)
        resultsFrame.pack(fill="both", expand=True, pady=20)

        resultsTitle = ctk.CTkLabel(resultsFrame, text="Results", font=("Arial", 20, "bold"))
        resultsTitle.pack(pady=(0, 10))

        self.resultsBox = ctk.CTkScrollableFrame(resultsFrame, width=300)
        self.resultsBox.pack(expand=True, fill="both")

        # Button to create a food
        createFoodBtn = ctk.CTkButton(left, text="Create New Food", command=lambda: controller.showFrame("InsertFood"))
        createFoodBtn.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Right panel
        self.right = ctk.CTkFrame(self)
        self.right.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.rightTitle = ctk.CTkLabel(self.right, text="Select a food…", font=("Arial", 24))
        self.rightTitle.pack(pady=10)

        # Info frame, hidden until
        self.infoFrame = ctk.CTkFrame(self.right, fg_color="transparent")
        self.infoFrame.pack(fill="x", pady=10)

        self.weightEntry = ctk.CTkEntry(self.right, placeholder_text="Enter weight in grams")
        self.submitBtn = ctk.CTkButton(self.right, text="Submit", command=self.submitFoodLog)

    def searchFoods(self):
        brand = self.brandEntry.get()
        name = self.nameEntry.get()

        response = self.getData.getFoodLike(brand, name)

        # Clear previous results
        for w in self.resultsBox.winfo_children():
            w.destroy()

        if not response["success"]:
            raise response["message"]

        data = response["data"]

        if not data:
            ctk.CTkLabel(self.resultsBox, text="No matching foods found.").pack()
            return

        # Add each result as a clickable row
        for foodMap in data:
            food = Food(
                foodMap["foodID"],
                foodMap["brand"],
                foodMap["name"],
                foodMap["calories"],
                foodMap["protein"],
                foodMap["carbs"],
                foodMap["fat"]
            )
            btn = ctk.CTkButton(
                self.resultsBox,
                text=f"{food.brand} - {food.name} (100g)",
                command=lambda f=food: self.selectFood(f),
                fg_color="#333333",
                hover_color="#444444"
            )
            btn.pack(fill="x", pady=5)

    def selectFood(self, food):
        self.selectedFood = food

        # Update the right panel UI
        for w in self.infoFrame.winfo_children():
            w.destroy()

        self.rightTitle.configure(text=f"{food.brand} - {food.name}")

        ctk.CTkLabel(self.infoFrame, text=f"Serving: 100g", font=("Arial", 16)).pack(anchor="w")
        ctk.CTkLabel(self.infoFrame, text=f"Calories: {(food.calories * 100):.2f}", font=("Arial", 16)).pack(anchor="w")
        ctk.CTkLabel(self.infoFrame, text=f"Protein: {(food.protein * 100):.2f}g", font=("Arial", 16)).pack(anchor="w")
        ctk.CTkLabel(self.infoFrame, text=f"Carbs: {(food.carbs * 100):.2f}g", font=("Arial", 16)).pack(anchor="w")
        ctk.CTkLabel(self.infoFrame, text=f"Fat: {(food.fat * 100):.2f}g", font=("Arial", 16)).pack(anchor="w")

        # Show weight entry and submit button
        self.weightEntry.pack(pady=10)
        self.submitBtn.pack(pady=5)

    def submitFoodLog(self):
        if not self.selectedFood:
            return

        weight = int(self.weightEntry.get())
        foodId = self.selectedFood.foodID

        response = self.userSubmissions.insertFoodLog(self.controller.username, foodId, weight, self.controller.selectedDate)

        if not response["success"]:
            raise response["message"]

        self.controller.showFrame("Dashboard")
        
    def clearInput(self):
        self.nameEntry.delete(0, "end")
        self.brandEntry.delete(0, "end")
        self.weightEntry.delete(0, "end")