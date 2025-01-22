from healthcare_db import get_connection

def add_conversation(doctor_id, patient_id, summary):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO conversations (doctor_id, patient_id, summary)
            VALUES (?, ?, ?)
        """, (doctor_id, patient_id, summary))
        conn.commit()

        print("Conversation added successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error adding conversation: {e}")
    finally:
        conn.close()
