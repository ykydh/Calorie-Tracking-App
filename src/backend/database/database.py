#Programmed by Aiden Pickett

import sqlite3

#Creates the database so sqlite3 library can be used
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

#Enables foreign keys. This is off by default within sqlite3
cursor.execute("PRAGMA foreign_keys = ON;")

#Creates the database to be used.
#Parameter type: None, void function.
def createDatabase():
    
    #Account
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Account (
            USERNAME VARCHAR(80) PRIMARY KEY,
            EMAIL VARCHAR(255) UNIQUE NOT NULL,
            PASSWORD_HASH VARCHAR(64) NOT NULL
        );
    """)

    #User
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            USERNAME VARCHAR(80) PRIMARY KEY,
            DOB DATE,
            GOAL_WEIGHT INTEGER,
            GOAL_DATE DATE,
            FOREIGN KEY (USERNAME) REFERENCES Account(USERNAME) ON DELETE CASCADE
        );
    """)

    #Food
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Food (
            FOOD_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT,
            BRAND TEXT,
            CALORIES DECIMAL(4,3) NOT NULL,
            FAT DECIMAL(3,3),
            PROTEIN DECIMAL(3,3),
            CARBS DECIMAL(3,3)
        );
    """)
    
    #Exercise
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Exercise (
            EXERCISE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TYPE VARCHAR(1)
        );
    """)

    #Cardio
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cardio (
            CARDIO_ID INTEGER PRIMARY KEY,
            NAME TEXT,
            CALORIES_BURNED_PER_MINUTE INTEGER,
            FOREIGN KEY (CARDIO_ID) REFERENCES Exercise(EXERCISE_ID) ON DELETE CASCADE
        );
    """)

    #Lifting
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Lifting (
            LIFT_ID INTEGER PRIMARY KEY,
            NAME TEXT,
            MUSCLES_WORKED TEXT,
            FOREIGN KEY (LIFT_ID) REFERENCES Exercise(EXERCISE_ID) ON DELETE CASCADE
        );
    """)
    
    #Food Log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Food_Log (
            LOG_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            OWNER_USERNAME VARCHAR(80) NOT NULL,
            FOOD_ID INTEGER NOT NULL,
            WEIGHT INTEGER,
            ATE_ON DATE,
            FOREIGN KEY (OWNER_USERNAME) REFERENCES Account(USERNAME) ON DELETE CASCADE,
            FOREIGN KEY (FOOD_ID) REFERENCES Food(FOOD_ID) ON DELETE CASCADE
        );
    """)

    #Exercise Log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Exercise_Log (
            E_LOG_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            EXERCISE_ID INTEGER NOT NULL,
            OWNER_USERNAME VARCHAR(80) NOT NULL,
            PERFORMED_ON DATE,
            FOREIGN KEY (OWNER_USERNAME) REFERENCES Account(USERNAME) ON DELETE CASCADE,
            FOREIGN KEY (EXERCISE_ID) REFERENCES Exercise(EXERCISE_ID) ON DELETE CASCADE
        );
    """)

    #Weight Log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Weight_Log (
            W_LOG_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            OWNER_USERNAME VARCHAR(80) NOT NULL,
            WEIGHT INT,
            LOGGED_ON DATE
        );
    """)

    #Height Log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Height_Log (
            H_LOG_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            OWNER_USERNAME VARCHAR(80) NOT NULL,
            HEIGHT INT,
            LOGGED_ON DATE
        );
    """)

    conn.commit()

#Clears the database in the case of the program being restarted
#Parameter Type: None, void function
def clearDatabase():
    tables = [
        "Height_Log",
        "Weight_Log"
        "Lifting",
        "Cardio",
        "User",
        "Exercise_log",
        "Food_log",
        "Food_barcodes",
        "Food",
        "Exercise",
        "Account"
    ]
    
    for table in tables:
        cursor.execute(f"""
            DROP TABLE IF EXISTS {table};
        """)
    
    conn.commit()

def initalizeDatabase():
    testPassHash = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"  # "test"

    # Food Samples
    foods = [
        ("bread", "wonder", 2.456, .026, .509, .088),
        ("sirloin tip steak", "beef choice", 2.143, .143, 0, .196),
        ("eggs", "great value", 1.4, .1, 0, .12),
        ("whole milk", "central dairy", .625, .033, .05, .033),
        ("butter", "land o lakes", 7.143, .786, 0, 0),
        ("sugar", "in the raw", 3.75, 0, 1, 0),
        ("flour", "bobs red mill", 3.529, .015, .735, .118)
    ]

    cursor.executemany(
        """
            INSERT INTO Food (NAME, BRAND, CALORIES, FAT, CARBS, PROTEIN)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        foods
    )

    # Account
    cursor.execute(
        f"""
            INSERT INTO Account (USERNAME, EMAIL, PASSWORD_HASH)
            VALUES ("test", "test@test.com", "{testPassHash}")
        """
    )

    # User
    cursor.execute(
        """
            INSERT INTO User (USERNAME, DOB, GOAL_WEIGHT, GOAL_DATE)
            VALUES ("test", "2004-01-01", 180, "2026-06-01")
        """
    )

    # Exercises
    cursor.executemany(
        """INSERT INTO Exercise (TYPE) VALUES (?)""",
        [
            ("C",),  # Cardio
            ("C",),  # Cardio
            ("L",),  # Lifting
            ("L",)   # Lifting
        ]
    )

    # Cardio
    cursor.execute(
        """
            INSERT INTO Cardio (CARDIO_ID, NAME, CALORIES_BURNED_PER_MINUTE)
            VALUES (1, "Running", 12)
        """
    )
    cursor.execute(
        """
            INSERT INTO Cardio (CARDIO_ID, NAME, CALORIES_BURNED_PER_MINUTE)
            VALUES (2, "Cycling", 8)
        """
    )

    # Lifting
    cursor.execute(
        """
            INSERT INTO Lifting (LIFT_ID, NAME, MUSCLES_WORKED)
            VALUES (3, "Bench Press", "Chest, Triceps")
        """
    )
    cursor.execute(
        """
            INSERT INTO Lifting (LIFT_ID, NAME, MUSCLES_WORKED)
            VALUES (4, "Squat", "Legs, Glutes")
        """
    )

    # Food Log
    cursor.executemany(
        """
            INSERT INTO Food_Log (OWNER_USERNAME, FOOD_ID, WEIGHT, ATE_ON)
            VALUES ("test", ?, ?, ?)
        """,
        [
            (1, 50, "2025-01-01"),
            (2, 200, "2025-01-01"),
            (3, 60, "2025-01-02")
        ]
    )

    # Exercise Log
    cursor.executemany(
        """
            INSERT INTO Exercise_Log (EXERCISE_ID, OWNER_USERNAME, PERFORMED_ON)
            VALUES (?, "test", ?)
        """,
        [
            (1, "2025-01-01"),  # Running
            (3, "2025-01-02")   # Bench Press
        ]
    )

    # Weight log
    cursor.executemany(
        """
            INSERT INTO Weight_Log (OWNER_USERNAME, WEIGHT, LOGGED_ON)
            VALUES ("test", ?, ?)
        """,
        [
            (190, "2025-01-01"),
            (188, "2025-02-01")
        ]
    )

    # Height log
    cursor.executemany(
        """
            INSERT INTO Height_Log (OWNER_USERNAME, HEIGHT, LOGGED_ON)
            VALUES ("test", ?, ?)
        """,
        [
            (70, "2025-01-01")  # 70 inches
        ]
    )

    conn.commit()
