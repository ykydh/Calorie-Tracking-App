import customtkinter as ctk

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

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
        rightFrame.grid_rowconfigure(0, weight=1)  # Exercise + Macros top
        rightFrame.grid_rowconfigure(1, weight=1)  # Weight Graph bottom
        rightFrame.grid_columnconfigure(0, weight=1)

        # Container for top half of right side container
        topRight = ctk.CTkFrame(rightFrame, fg_color="transparent")
        topRight.grid(row=0, column=0, sticky="nsew")
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

        ctk.CTkLabel(macrosFrame, text="Calories Remaining").pack()
        self.calBar = ctk.CTkProgressBar(macrosFrame, width=250)
        self.calBar.set(0.4)
        self.calBar.pack(pady=5)

        ctk.CTkLabel(macrosFrame, text="Protein").pack()
        self.proteinBar = ctk.CTkProgressBar(macrosFrame, width=250)
        self.proteinBar.set(0.6)
        self.proteinBar.pack(pady=5)

        ctk.CTkLabel(macrosFrame, text="Carbs").pack()
        self.carbsBar = ctk.CTkProgressBar(macrosFrame, width=250)
        self.carbsBar.set(0.2)
        self.carbsBar.pack(pady=5)

        ctk.CTkLabel(macrosFrame, text="Fats").pack()
        self.fatsBar = ctk.CTkProgressBar(macrosFrame, width=250)
        self.fatsBar.set(0.5)
        self.fatsBar.pack(pady=5)

        macrosFrame.bind("<Button-1>", lambda e: controller.showMacrosScreen())

        # Weight graph
        bottomRight = ctk.CTkFrame(rightFrame, corner_radius=15)
        bottomRight.grid(row=1, column=0, sticky="nsew", pady=(10,0))
        bottomRight.grid_rowconfigure(0, weight=1)
        bottomRight.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(bottomRight, text="Weight Progress", font=("Arial", 28)).pack(pady=10)

        self.weightGraph = ctk.CTkFrame(bottomRight, height=250, fg_color="#1e1e1e")
        self.weightGraph.pack(expand=True, fill="both", padx=10, pady=10)

        self.weightGraph.bind("<Button-1>", lambda e: controller.showWeightScreen())

        # ---------------- PROFILE BUTTON ----------------
        profileBtn = ctk.CTkButton(
            self, text="👤", width=50, height=50,
            fg_color="transparent", hover_color="#333333",
            command=None
        )
        profileBtn.place(relx=0.97, rely=0.03, anchor="ne")
