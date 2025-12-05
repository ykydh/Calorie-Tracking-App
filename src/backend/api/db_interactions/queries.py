class Queries:
    # GETS
    GET_USER_FROM_USERNAME = """
        SELECT PASSWORD_HASH
        FROM ACCOUNT
        WHERE USERNAME = :username
    """
    
    GET_USER_FROM_EMAIL = """
        SELECT PASSWORD_HASH
        FROM ACCOUNT
        WHERE EMAIL = :email
    """
    
    # INSERTS
    
    # MODIFICATIONS
    
    # DELETES