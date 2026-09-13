from database.db import get_connection


from werkzeug.security import check_password_hash

def get_user_by_email(email):
    
    conn=get_connection()
    
    try:
        cursor=conn.cursor(dictionary=True)
        
        query="""
            SELECT
                id,
                name,
                email,
                password_hash,
                role,
                status,
                created_at
            FROM users
            WHERE email = %s
            LIMIT 1
        """
        cursor.execute(query, (email,))

        user = cursor.fetchone()

        return user
    finally:
        cursor.close()
        conn.close()
        
        
        
def authenticate_user(email,password):
    user= get_user_by_email(email)
    # check if the user exists
    if user is None:
        return None
    # check if the user is active
    if user['status'] != 'active':
        return None
    # check if the password is correct
    password_correct=check_password_hash(user['password_hash'],password)
    
    # if the password is correct, return the user
    if password_correct:
        return user
    
    return None
    
    

    