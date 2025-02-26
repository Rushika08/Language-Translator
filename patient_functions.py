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

def add_patient(username, password, name, date_of_birth, gender, contact_info, language, email=None):
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


def get_patient_history(patient_username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.name, p.date_of_birth, p.gender, d.name, c.created_at, c.summary, 
            c.conversation_id, c.patient_id, p.contact_info, d.contact_info, p.language
        FROM conversations AS c
        INNER JOIN patients AS p ON c.patient_id = p.patient_id
        INNER JOIN doctors AS d ON c.doctor_id = d.doctor_id
        WHERE c.patient_id = ?
    """, (patient_username,))
    
    records = cursor.fetchall()
    conn.close()

    patient_history = []
    for record in records:
        patient_history.append({
            "patient_name": record[0],
            "date_of_birth": record[1],
            "gender": record[2],
            "doctor_name": record[3],
            "date": record[4],
            "summary": record[5],
            "conversation_id": record[6],
            "patient_id": record[7],
            "patient_contact_info": record[8],
            "doctor_contact_info": record[9],
            "patient_language": record[10]
        })

    return patient_history

def add_patient_visit(doctor_id, patient_username, summary):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id
        FROM users
        WHERE username = ?
    """, (patient_username,))

    patient_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO conversations (doctor_id, patient_id, summary)
        VALUES (?, ?, ?)
    """, (doctor_id, patient_id, summary))
    
    conn.close()
    return "Patient visit added successfully."
                   
    