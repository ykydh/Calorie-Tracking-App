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
            CALORIES DECIMAL(3,3) NOT NULL,
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


# def initalizeDatabase():
