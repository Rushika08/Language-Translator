import sqlite3

conn = sqlite3.connect("healthcare_system.db")
cursor = conn.cursor()
# username = 'admin'
cursor.execute("""
        SELECT *
        FROM users
    """)

users = cursor.fetchall()

# patients = [{"name": row[0], "contact_info": row[1], "gender": row[2], "date_of_birth": row[3]} for row in cursor.fetchall()]
print(users)
conn.close()