class Queries:
    # GETS
    # Gets user info when given a username
    GET_USER_FROM_USERNAME = """
        SELECT 
            a.PASSWORD_HASH as hash, 
            a.USERNAME AS username,
            u.GOAL_WEIGHT AS goalWeight, 
            u.GOAL_DATE AS goalDate,
            u.DOB AS dob
        FROM Account a
        INNER JOIN User u
            ON a.USERNAME = u.USERNAME
        WHERE a.USERNAME = :username
    """
    
    # Gets user info when given an email
    GET_USER_FROM_EMAIL = """
        SELECT 
            a.PASSWORD_HASH as hash, 
            a.USERNAME AS username,
            u.GOAL_WEIGHT AS goalWeight, 
            u.GOAL_DATE AS goalDate,
            u.DOB AS dob
        FROM Account a
        INNER JOIN User u
            ON a.USERNAME = u.USERNAME
        WHERE a.EMAIL = :email
    """

    # Given a date, and username, it gets users logs and info at the specified date
    GET_USER_INFO_AT_TIME = """
        SELECT
            u.USERNAME,
            wl.WEIGHT AS weight,
            hl.HEIGHT AS height,
            u.GOAL_WEIGHT AS goalWeight,
            u.DOB AS dob,
            u.GOAL_DATE AS goalDate
        FROM User u
        LEFT JOIN (
            SELECT OWNER_USERNAME, WEIGHT
            FROM Weight_Log
            WHERE (OWNER_USERNAME, LOGGED_ON) IN (
                SELECT OWNER_USERNAME, MAX(LOGGED_ON)
                FROM Weight_Log
                WHERE LOGGED_ON <= :date
                GROUP BY OWNER_USERNAME
            )
        ) wl ON wl.OWNER_USERNAME = u.USERNAME
        LEFT JOIN (
            SELECT OWNER_USERNAME, HEIGHT
            FROM Height_Log
            WHERE (OWNER_USERNAME, LOGGED_ON) IN (
                SELECT OWNER_USERNAME, MAX(LOGGED_ON)
                FROM Height_Log
                WHERE LOGGED_ON <= :date
                GROUP BY OWNER_USERNAME
            )
        ) hl ON hl.OWNER_USERNAME = u.USERNAME
        WHERE u.USERNAME = :username
    """

    # Gets food logs for user given username and a date
    GET_FOOD_LOGS = """
        SELECT 
            LOG_ID AS logID,
            FOOD_ID AS foodID
        FROM Food_Log
        WHERE
            ATE_ON = :date AND
            OWNER_USERNAME = :username
        
    """

    # Calculates information like the total calories, protein, carbs, and fat about a food log given the food logs id
    GET_LOG_INFO = """
        SELECT 
            f.BRAND AS brand,
            f.NAME AS name,
            fl.WEIGHT AS weight,
            IFNULL((fl.WEIGHT * f.CALORIES), 0) AS logCalories,
            IFNULL((fl.WEIGHT * f.PROTEIN), 0) AS logProtein,
            IFNULL((fl.WEIGHT * f.CARBS), 0) AS logCarbs,
            IFNULL((fl.WEIGHT * f.FAT), 0) AS logFat
        FROM Food_Log fl
        INNER JOIN Food f
            ON fl.FOOD_ID = f.FOOD_ID
        WHERE fl.LOG_ID = :logID
        ORDER BY name DESC
    """

    # Gets the total amount of protein, calories, carbs, and fat, a user has eaten on a specific date
    GET_DAILY_INFO = """
        SELECT 
            IFNULL(SUM(fl.WEIGHT * f.CALORIES), 0) AS totalCalories,
            IFNULL(SUM(fl.WEIGHT * f.PROTEIN), 0) AS totalProtein,
            IFNULL(SUM(fl.WEIGHT * f.CARBS), 0) AS totalCarbs,
            IFNULL(SUM(fl.WEIGHT * f.FAT), 0) AS totalFat
        FROM Food_Log fl
        INNER JOIN Food f
            ON fl.FOOD_ID = f.FOOD_ID
        WHERE 
            fl.ATE_ON = :date AND 
            fl.OWNER_USERNAME = :username
    """

    # Searches for foods in the database similar to the brand and name, is not case sensitive, and matches anything with characters in same order
    GET_FOODS_LIKE = """
        SELECT 
            FOOD_ID AS foodID,
            NAME AS name,
            BRAND AS brand,
            CALORIES AS calories,
            FAT AS fat,
            PROTEIN AS protein,
            CARBS AS carbs
        FROM Food
        WHERE (:brand = '' OR BRAND LIKE '%' || :brand || '%' COLLATE NOCASE) AND 
        (:name = '' OR NAME  LIKE '%' || :name || '%' COLLATE NOCASE)
    """

    # Gets exercise logs on a specific date
    GET_EXERCISE_LOGS_ON = """
        SELECT 
            el.E_LOG_ID AS logID,
            el.EXERCISE_ID AS exerciseID,
            el.PERFORMED_FOR AS minutes,
            e.TYPE as type
        FROM Exercise_Log el
        INNER JOIN Exercise e 
        ON el.EXERCISE_ID = e.EXERCISE_ID
        WHERE
            el.PERFORMED_ON = :date AND
            el.OWNER_USERNAME = :username
    """

    # Gets cardio exercise
    GET_CARDIO = """
        SELECT
            NAME as name,
            CALORIES_BURNED_PER_MINUTE AS cbpm
        FROM Cardio
        WHERE CARDIO_ID = :id
    """

    # Gets lifting exercise
    GET_LIFT = """
        SELECT
            NAME as name,
            MUSCLES_WORKED AS musclesWorked
        FROM Lifting
        WHERE LIFT_ID = :id
    """

    # Gets the calories burned for a user on a specific date, given a date and username
    GET_CALORIES_BURNED_ON = """
        SELECT 
            SUM(c.CALORIES_BURNED_PER_MINUTE * el.PERFORMED_FOR) AS totalCalsBurned
        FROM Exercise_Log el
        INNER JOIN Exercise e 
            ON el.EXERCISE_ID = e.EXERCISE_ID
        INNER JOIN Cardio c 
            ON e.EXERCISE_ID = c.CARDIO_ID
        WHERE 
            el.OWNER_USERNAME = :username
            AND el.PERFORMED_ON = :date;
    """

    # Searches for exercises similar to name entered, is not case sensitive and matches characters in same order
    GET_EXERCISES_LIKE = """
        SELECT
            e.EXERCISE_ID AS exerciseID,
            e.TYPE AS type,
            COALESCE(c.NAME, l.NAME) AS name,
            c.CALORIES_BURNED_PER_MINUTE AS caloriesPerMinute,
            l.MUSCLES_WORKED AS musclesWorked
        FROM Exercise e
        LEFT JOIN Cardio c 
            ON e.EXERCISE_ID = c.CARDIO_ID
        LEFT JOIN Lifting l
            ON e.EXERCISE_ID = l.LIFT_ID
        WHERE
            (:name = '' OR (c.NAME LIKE '%' || :name || '%' COLLATE NOCASE) OR (l.NAME LIKE '%' || :name || '%' COLLATE NOCASE));
    """
    
    # Gets weight logs for a user
    GET_WEIGHT_LOGS = """
        SELECT
            W_LOG_ID AS logID,
            WEIGHT AS weight,
            LOGGED_ON AS date
        FROM Weight_Log
        WHERE OWNER_USERNAME = :username
        ORDER BY LOGGED_ON ASC;
    """
    
    # Gets users date of birth, and most recent height
    GET_DOB_AND_HEIGHT = """
        SELECT
            u.DOB AS dob,
            hl.HEIGHT AS height
        FROM User u
        LEFT JOIN Height_Log hl
        ON u.USERNAME = hl.OWNER_USERNAME
        WHERE u.USERNAME = :username
        ORDER BY hl.LOGGED_ON
    """
    
    # INSERTS
    # Inserts a user to account table
    INSERT_USER_TO_ACCOUNT = """
        INSERT INTO Account (EMAIL, USERNAME, PASSWORD_HASH)
        VALUES (:email, :username, :hash)
    """

    # Inserts user to the user table
    INSERT_USER_TO_USER = """
        INSERT INTO User (USERNAME)
        VALUES (:username)
    """
    
    # Inserts a weight log to the weight log table
    INSERT_WEIGHT_LOG = """
        INSERT INTO Weight_Log (WEIGHT, OWNER_USERNAME, LOGGED_ON)
        VALUES(:weight, :username, :date)
    """

    # Inserts a height log to the height log table
    INSERT_HEIGHT_LOG = """
        INSERT INTO Height_Log (HEIGHT, OWNER_USERNAME, LOGGED_ON)
        VALUES(:height, :username, :date)
    """

    # Inserts a food log to the food log table
    INSERT_FOOD_LOG = """
        INSERT INTO Food_Log (OWNER_USERNAME, FOOD_ID, WEIGHT, ATE_ON)
        VALUES(:username, :foodID, :weight, :date)
    """

    # Inserts a exercise log to the exercise log table
    INSERT_EXERCISE_LOG = """
        INSERT INTO Exercise_Log (OWNER_USERNAME, EXERCISE_ID, PERFORMED_FOR, PERFORMED_ON)
        VALUES(:username, :exerciseID, :minutes, :date)
    """

    # Inserts a exercise to the exercise table
    INSERT_EXERCISE = """
        INSERT INTO Exercise (TYPE)
        VALUES(:type)
    """

    # Inserts cardio to the cardio table
    INSERT_CARDIO = """
        INSERT INTO Cardio (NAME, CALORIES_BURNED_PER_MINUTE)
        VALUES(:type, :cbpm)
    """

    # Inserts lift to the lift table
    INSERT_LIFT = """
        INSERT INTO Lift (NAME, MUSCLES_WORKED)
        VALUES(:name, :musclesWorked)
    """
    
    # Inserts a food to the food table
    INSERT_FOOD = """
        INSERT INTO Food (NAME, BRAND, CALORIES, PROTEIN, CARBS, FAT)
        VALUES (:name, :brand, :unitCals, :unitProtein, :unitCarbs, :unitFat)
    """
    
    # MODIFICATIONS
    # Updates users date of birth given a username and a new date
    UPDATE_DOB = """
        UPDATE User 
        SET DOB = :dob
        WHERE USERNAME = :username
    """

    # Updates users goal weight given their username and a new goal weight
    UPDATE_GOAL_WEIGHT = """
        UPDATE User 
        SET GOAL_WEIGHT = :goalWeight
        WHERE USERNAME = :username
    """

    # Updates users goal date given username a new goal date
    UPDATE_GOAL_DATE = """
        UPDATE User 
        SET GOAL_DATE = :goalDate
        WHERE USERNAME = :username
    """
    
    # Updates weight on a food log given the new weight and the log id
    UPDATE_FOOD_LOG = """
        UPDATE Food_Log
        SET WEIGHT = :newWeight
        WHERE LOG_ID = :logID
    """
    
    # Updates time spent on exercise given new time and the log ID
    UPDATE_EXERCISE_LOG = """
        UPDATE Exercise_Log
        SET PERFORMED_FOR = :newTime
        WHERE E_LOG_ID = :logID
    """
    
    # DELETES
    # Deletes food log from the users logs
    DELETE_FOOD_LOG = """
        DELETE 
        FROM Food_Log
        WHERE LOG_ID = :id
    """
    
    # Deletes exercise log from the users logs
    DELETE_EXERCISE_LOG = """
        DELETE 
        FROM Exercise_Log
        WHERE E_LOG_ID = :id
    """