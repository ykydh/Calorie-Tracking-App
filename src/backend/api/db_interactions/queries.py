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
        WHERE a.USERNAME = :username;
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
        WHERE a.EMAIL = :email;
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
            FOOD_ID AS foodID,
        FROM Food_Log
        WHERE
            ATE_ON = :date AND
            OWNER_USERNAME = :username
    """

    GET_LOG_INFO = """
        SELECT 
            f.BRAND AS brand,
            f.NAME AS name,
            IFNULL((fl.WEIGHT * f.CALORIES), 0) AS logCaloires,
            IFNULL((fl.WEIGHT * f.PROTEIN), 0) AS logProtein,
            IFNULL((fl.WEIGHT * f.CARBS), 0) AS logCarbs,
            IFNULL((fl.WEIGHT * f.FAT), 0) AS logFat
        FROM Food_Log fl
        INNER JOIN Food f
            ON fl.FOOD_ID = f.FOOD_ID
        WHERE fl.LOG_ID = :logID
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
    
    # INSERTS
    INSERT_USER_TO_ACCOUNT = """
        INSERT INTO Account (EMAIL, USERNAME, PASSWORD_HASH)
        VALUES (:email, :username, :hash);
    """

    INSERT_USER_TO_USER = """
        INSERT INTO User (USERNAME)
        VALUES (:username);
    """
    
    INSERT_WEIGHT_LOG = """
        INSERT INTO Weight_Log (WEIGHT, OWNER_USERNAME, LOGGED_ON)
        VALUES(:weight, :username, :date)
    """

    INSERT_HEIGHT_LOG = """
        INSERT INTO Height_Log (HEIGHT, OWNER_USERNAME, LOGGED_ON)
        VALUES(:height, :username, :date)
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