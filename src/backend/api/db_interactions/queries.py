class Queries:
    # GETS
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

    GET_FOOD_LOGS = """
        SELECT 
            LOG_ID AS logID,
            FOOD_ID AS foodID
        FROM Food_Log
        WHERE
            ATE_ON = :date AND
            OWNER_USERNAME = :username
        
    """

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

    GET_EXERCISE_LOGS_ON = """
        SELECT 
            el.E_LOG_ID AS logID,
            el.EXERCISE_ID AS exerciseID,
            el.PERFORMED_FOR AS minutes,
            e.TYPE as type
        FROM Exercise_Log el
        INNER JOIN Exercise e 
        ON (el.EXERCISE_ID = e.EXERCISE_ID)
        WHERE
            el.PERFORMED_ON = :date AND
            el.OWNER_USERNAME = :username
    """

    GET_CARDIO = """
        SELECT
            NAME as name,
            CALORIES_BURNED_PER_MINUTE AS cbpm
        FROM Cardio
        WHERE CARDIO_ID = :id
    """

    GET_LIFT = """
        SELECT
            NAME as name,
            MUSCLES_WORKED AS musclesWorked
        FROM Lifting
        WHERE LIFT_ID = :id
    """

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

    GET_WEIGHT_LOGS = """
        SELECT
            W_LOG_ID AS logID,
            WEIGHT AS weight,
            LOGGED_ON AS date
        FROM Weight_Log
        WHERE OWNER_USERNAME = :username
        ORDER BY LOGGED_ON ASC;
    """
    
    # INSERTS
    INSERT_USER_TO_ACCOUNT = """
        INSERT INTO Account (EMAIL, USERNAME, PASSWORD_HASH)
        VALUES (:email, :username, :hash)
    """

    INSERT_USER_TO_USER = """
        INSERT INTO User (USERNAME)
        VALUES (:username)
    """
    
    INSERT_WEIGHT_LOG = """
        INSERT INTO Weight_Log (WEIGHT, OWNER_USERNAME, LOGGED_ON)
        VALUES(:weight, :username, :date)
    """

    INSERT_HEIGHT_LOG = """
        INSERT INTO Height_Log (HEIGHT, OWNER_USERNAME, LOGGED_ON)
        VALUES(:height, :username, :date)
    """

    INSERT_FOOD_LOG = """
        INSERT INTO Food_Log (OWNER_USERNAME, FOOD_ID, WEIGHT, ATE_ON)
        VALUES(:username, :foodID, :weight, :date)
    """

    INSERT_EXERCISE_LOG = """
        INSERT INTO Exercise_Log (OWNER_USERNAME, EXERCISE_ID, PERFORMED_FOR, PERFORMED_ON)
        VALUES(:username, :exerciseID, :minutes, :date)
    """

    INSERT_EXERCISE = """
        INSERT INTO Exercise (TYPE)
        VALUES(:type)
    """

    INSERT_CARDIO = """
        INSERT INTO Cardio (NAME, CALORIES_BURNED_PER_MINUTE)
        VALUES(:type, :cbpm)
    """

    INSERT_LIFT = """
        INSERT INTO Lift (NAME, MUSCLES_WORKED)
        VALUES(:name, :musclesWorked)
    """
    
    # MODIFICATIONS
    UPDATE_DOB = """
        UPDATE User 
        SET DOB = :dob
        WHERE USERNAME = :username
    """

    UPDATE_GOAL_WEIGHT = """
        UPDATE User 
        SET GOAL_WEIGHT = :goalWeight
        WHERE USERNAME = :username
    """

    UPDATE_GOAL_DATE = """
        UPDATE User 
        SET GOAL_DATE = :goalDate
        WHERE USERNAME = :username
    """
    
    # DELETES