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
        EMAIL VARCHAR(80) NOT NULL,
        UID INT NOT NULL,
        PASSWORD VARCHAR(80) NOT NULL,
        HASH VARCHAR(80) NOT NULL,
        HASHCODE VARCHAR(80) NOT NULL,
        PRIMARY KEY (EMAIL)  
   );
    """)

    #Food Log
    cursor.execute("""
    CREATE TABLE Food_Log (
        LOGID INT NOT NULL,
        WEIGHT INT,
        MONTH VARCHAR(80),
        DATE INT,
        YEAR INT,
        TIME INT,
        PRIMARY KEY (LOGID)
   );
    """)


    #Exercise Log
    cursor.execute("""
    CREATE TABLE Exercise_Log (
        ELOGID INT NOT NULL,
        MONTH VARCHAR(80),
        DATE INT,
        YEAR INT,
        TIME INT,
        PRIMARY KEY (ELOGID),
   );
    """)

    #User
    cursor.execute("""
    CREATE TABLE User (
        UID INT NOT NULL,
        LOGID INT NOT NULL,
        ELOGID INT NOT NULL,
        WEIGHT INT,
        HEIGHT INT,
        DOB INT,
        GOALWEIGHT INT,
        PRIMARY KEY (UID),
        FOREIGN KEY (UID) REFERENCES Account(UID),
        FOREIGN KEY (LOGID) REFERENCES Food_Log(LOGID),
        FOREIGN KEY (ELOGID) REFERENCES Exercise_Log(ELOGID)
   );
    """)

    #Food
    cursor.execute("""
    CREATE TABLE Food (
        FOODID INT NOT NULL,
        LOGID INT NOT NULL,
        NAME VARCHAR(80),
        BRAND VARCHAR(80),
        CALORIES INT NOT NULL,
        FAT INT,
        PROTEIN INT,
        CARBS INT,
        PRIMARY KEY (FOODID),
        FOREIGN KEY (LOGID) REFERENCES Food_Log(LOGID)
   );
    """)

    #Food Barcodes
    cursor.execute("""
    CREATE TABLE Food_Barcodes (
        BARCODEID INT NOT NULL,
        FOODID INT NOT NULL,
        PRIMARY KEY (BARCODEID),
        FOREIGN KEY (FOODID) REFERENCES Food(FOODID)
   );
    """)

    #Cardio
    cursor.execute("""
    CREATE TABLE Cardio (
        EXERCISEID INT NOT NULL,
        ELOGID INT NOT NULL,
        NAME VARCHAR(80),
        PRIMARY KEY (EXERCISEID)
        FOREIGN KEY (ELOGID) REFERENCES Exercise_Log(ELOGID),
   );
    """)

    #Lifting
    cursor.execute("""
    CREATE TABLE Lifting (
        EXERCISEID INT NOT NULL,
        ELOGID INT NOT NULL,
        NAME VARCHAR(80),
        PRIMARY KEY (EXERCISEID)
        FOREIGN KEY (ELOGID) REFERENCES Exercise_Log(ELOGID),
   );
    """)

    conn.commit()

#Clears the database in the case of the program being restarted
#Parameter Type: None, void function
def clearDatabase():
    cursor.execute("""
        DROP TABLE IF EXISTS Lifting;
        DROP TABLE IF EXISTS Cardio;
        DROP TABLE IF EXISTS Food_Barcodes;
        DROP TABLE IF EXISTS Food;
        DROP TABLE IF EXISTS User;
        DROP TABLE IF EXISTS Exercise_Log;
        DROP TABLE IF EXISTS Food_Log;
        DROP TABLE IF EXISTS Account;
     """)
    
    conn.commit()


def initalizeDatabase():

