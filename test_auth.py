from database.db import get_connection
from database.auth import authenticate_user
from werkzeug.security import generate_password_hash



name = "Admin User"
email = "admin@test.com"
password = "Admin@123"
role = "admin"
status = "active"

# Convert the normal password into a secure hash.
password_hash = generate_password_hash(password)

conn = get_connection()
cursor = conn.cursor()

# Insert the user into the database
try:
    query = """
    INSERT INTO users (name, email, password_hash, role, status)
    VALUES (%s, %s, %s, %s, %s)
"""
    cursor.execute(query, (name, email, password_hash, role, status))
    conn.commit()
finally:
    cursor.close()
    conn.close()
    
    
user = authenticate_user('admin@test.com', 'Admin@123')

if user is not None:
    print("Authentication successful!")
    print(f"User ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, Role: {user['role']}, Status: {user['status']}")
else:
    print("Authentication failed.")