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
        CREATE TABLE Account (
            USERNAME VARCHAR(80) NOT NULL UNIQUE,
            EMAIL VARCHAR(80) NOT NULL UNIQUE,
            PASSWORD_HASH VARCHAR(64) NOT NULL,
            PRIMARY KEY (USERNAME)  
    );
    """)

    #User
    cursor.execute("""
    CREATE TABLE User (
        USERNAME VARCHAR(80) NOT NULL UNIQUE,
        WEIGHT INT,
        HEIGHT INT,
        DOB INT,
        GOALWEIGHT INT,
        PRIMARY KEY (USERNAME),
        FOREIGN KEY (USERNAME) REFERENCES Account(USERNAME) ON DELETE CASCADE
    );
    """)

    #Food
    cursor.execute("""
    CREATE TABLE Food (
        FOOD_ID INT NOT NULL AUTOINCREMENT UNIQUE,
        NAME VARCHAR(80),
        BRAND VARCHAR(80),
        CALORIES DECIMAL NOT NULL,
        FAT DECIMAL(3,3),
        PROTEIN DECIMAL(3,3),
        CARBS DECIMAL(3,3),
        PRIMARY KEY (FOOD_ID)
    );
    """)

    #Food Barcodes
    cursor.execute("""
    CREATE TABLE Food_Barcodes (
        BARCODE_ID INT NOT NULL UNIQUE,
        FOOD_ID INT NOT NULL,
        PRIMARY KEY (BARCODE_ID),
        FOREIGN KEY (FOOD_ID) REFERENCES Food(FOOD_ID) ON DELETE CASCADE
    );
    """)
    
    cursor.execute("""
    CREATE TABLE Exercise (
        EXERCISE_ID INT NOT NULL AUTOINCREMENT UNIQUE,
        TYPE VARCHAR,
        PRIMARY KEY (EXERCISE_ID) ON DELETE CASCADE
    );
    """)

    #Cardio
    cursor.execute("""
    CREATE TABLE Cardio (
        CARDIO_ID INT NOT NULL UNIQUE,
        NAME VARCHAR(80),
        CALORIES_BURNED_PER_MINUTE INT,
        PRIMARY KEY (EXERCISE_ID),
        FOREIGN KEY (CARDIO_ID) REFERENCES Exercise(EXERCISE_ID) ON DELETE CASCADE
    );
    """)

    #Lifting
    cursor.execute("""
    CREATE TABLE Lifting (
        LIFT_ID INT NOT NULL UNIQUE,
        NAME VARCHAR(80),
        MUSCLES_WORKED VARCHAR(80),
        PRIMARY KEY (EXERCISE_ID),
        FOREIGN KEY (LIFT_ID) REFERENCES Exercise(EXERCISE_ID) ON DELETE CASCADE
    );
    """)
    
    #Food Log
    cursor.execute("""
    CREATE TABLE Food_Log (
        LOG_ID INT NOT NULL AUTOINCREMENT UNIQUE,
        OWNER_USERNAME VARCHAR(80) NOT NULL,
        FOOD_ID INT NOT NULL,
        WEIGHT INT,
        MONTH VARCHAR(80),
        DATE INT,
        YEAR INT,
        TIME INT,
        PRIMARY KEY (LOG_ID),
        FOREIGN KEY (OWNER_USERNAME) REFERENCES Account(USERNAME) ON DELETE CASCADE,
        FOREGIN KEY (FOOD_ID) REFERENCES Food(FOOD_ID) ON DELETE CASCADE
    );
    """)

    #Exercise Log
    cursor.execute("""
    CREATE TABLE Exercise_Log (
        E_LOG_ID INT NOT NULL AUTOINCREMENT UNIQUE,
        EXERCISE_ID INT NOT NULL,
        OWNER_USERNAME VARCHAR(80) NOT NULL,
        MONTH VARCHAR(80),
        DATE INT,
        YEAR INT,
        TIME INT,
        PRIMARY KEY (E_LOG_ID),
        FOREIGN KEY (OWNER_USERNAME) REFERENCES Account(USERNAME) ON DELETE CASCADE,
        FOREIGN KEY (EXERCISE_ID) REFERENCES Exercise(EXERCISE_ID) ON DELETE CASCADE
    );
    """)

    conn.commit()

#Clears the database in the case of the program being restarted
#Parameter Type: None, void function
def clearDatabase():
    tables = [
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
