class Queries:
    # GETS
    GET_USER_FROM_USERNAME = """
        SELECT a.PASSWORD_HASH as hash, 
            a.USERNAME AS username,
            u.WEIGHT AS weight, 
            u.HEIGHT AS height, 
            u.GOAL_WEIGHT AS goalWeight, 
            u.DOB AS dob
        FROM Account a
        INNER JOIN User u
            ON (a.USERNAME = u.USERNAME)
        WHERE a.USERNAME = :username;
    """
    
    GET_USER_FROM_EMAIL = """
        SELECT a.PASSWORD_HASH as hash, 
            a.USERNAME AS username,
            u.WEIGHT AS weight, 
            u.HEIGHT AS height, 
            u.GOAL_WEIGHT AS goalWeight, 
            u.DOB AS dob
        FROM Account a
        INNER JOIN User u
            ON a.USERNAME = u.USERNAME
        WHERE a.EMAIL = :email;
    """
    
    # INSERTS
    INSERT_USER_TO_ACCOUNT = """
        INSERT INTO Account (EMAIL, USERNAME, PASSWORD_HASH)
        VALUES (:email, :username, :hash);
    """

    INSERT_USER_TO_USER = """
        INSERT INTO User (Username)
        VALUES (:username);
    """
    
    # MODIFICATIONS

    UPDATE_WEIGHT = """
        UPDATE User 
        SET WEIGHT = :weight
        WHERE USERNAME = :username
    """

    UPDATE_HEIGHT = """
        UPDATE User 
        SET HEIGHT = :height
        WHERE USERNAME = :username
    """

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
    
    # DELETES