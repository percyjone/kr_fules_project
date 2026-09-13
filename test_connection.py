from database.db import get_connection


try:

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM tank"
    )

    result = cursor.fetchone()

    print(
        "MYSQL CONNECTION SUCCESSFUL"
    )

    print(
        "Tank table row count:",
        result[0]
    )

    cursor.close()

    conn.close()

except Exception as e:

    print(
        "DATABASE TEST FAILED:"
    )

    print(e)