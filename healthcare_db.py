import sqlite3
import bcrypt
# from user_functions import hash_password

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def get_connection():
    # Establish and return a connection to the database
    return sqlite3.connect("healthcare_system.db")

def create_tables():
    # Create the necessary tables
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('Admin', 'Doctor', 'Patient')) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            contact_info TEXT,
            language TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            date_of_birth DATE NOT NULL,
            gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')) NOT NULL,
            contact_info TEXT,
            language TEXT,
            email TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            summary TEXT,
            FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
        );
    """)

    print("Tables created successfully.")

    # Insert admin user if not exists
    cursor.execute("""
        SELECT * FROM users WHERE role = 'Admin' LIMIT 1
    """)
    admin_exists = cursor.fetchone()

    if not admin_exists:
        # Insert an admin user if no admin exists
        admin_username = 'admin'
        admin_password = 'admin123'  # Ensure this is a hashed password
        admin_role = 'Admin'
        cursor.execute("""
            INSERT INTO users (username, password, role) 
            VALUES (?, ?, ?)
        """, (admin_username, admin_password, admin_role))
        conn.commit()  # Commit the changes before closing
        print("Admin user created successfully.")
    
    conn.close()
