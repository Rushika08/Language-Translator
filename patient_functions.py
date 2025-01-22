from healthcare_db import get_connection


def add_patient(username, password, name, date_of_birth, gender, contact_info, language):
    # Insert the new patient into the database
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (username, password, "Patient"))
    
    user_id = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO patients (user_id, name, date_of_birth, gender, contact_info, language)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, name, date_of_birth, gender, contact_info, language))

    conn.commit()
    conn.close()

def add_patient(username, password, name, date_of_birth, gender, contact_info, language):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Add user
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (username, password, "Patient"))
        user_id = cursor.lastrowid

        # Add patient
        cursor.execute("""
            INSERT INTO patients (user_id, name, date_of_birth, gender, contact_info, language)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, name, date_of_birth, gender, contact_info, language))
        conn.commit()

        print(f"Patient {name} added successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error adding patient: {e}")
    finally:
        conn.close()


def get_all_patients():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, contact_info, gender, date_of_birth 
        FROM patients
    """)
    patients = [{"name": row[0], "contact_info": row[1], "gender": row[2], "date_of_birth": row[3]} for row in cursor.fetchall()]

    conn.close()
    return patients


def get_patient_history(patient_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, summary
        FROM conversations
        WHERE patient_id = (SELECT patient_id FROM patients WHERE name = ?)
    """, (patient_name,))
    
    records = cursor.fetchall()
    conn.close()

    patient_history = []
    for record in records:
        patient_history.append({
            "date": record[0],
            "summary": record[1]
        })

    return patient_history

