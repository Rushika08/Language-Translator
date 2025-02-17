from healthcare_db import get_connection
import streamlit as st
from patient_functions import get_patient_history, add_patient, add_patient_visit

def get_doctor_info(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT d.doctor_id, d.user_id, u.username, d.name, d.specialization, d.contact_info, d.language
        FROM doctors AS d
        INNER JOIN users AS u ON d.user_id = u.user_id
        WHERE username = ?
    """, (username,))
    
    doctor_info = cursor.fetchone()
    conn.close()
    
    if doctor_info:
        return {
            "doctor_id": doctor_info[0],
            "user_id": doctor_info[1],
            "username": doctor_info[2],
            "name": doctor_info[3],
            "specialization": doctor_info[4],
            "contact_info": doctor_info[5],
            "language": doctor_info[6]
        }
    return None


def add_doctor(username, password, name, specialization, contact_info, language):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Add user
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (username, password, "Doctor"))
        user_id = cursor.lastrowid

        # Add doctor
        cursor.execute("""
            INSERT INTO doctors (user_id, name, specialization, contact_info, language)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, name, specialization, contact_info, language))
        conn.commit()

        print(f"Doctor {name} added successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error adding doctor: {e}")
    finally:
        conn.close()

def get_all_doctors():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, specialization, contact_info, user_id, doctor_id, language
        FROM doctors
    """)
    doctors = [{"name": row[0], "specialization": row[1], "contact_info": row[2], "user_id": row[3], "doctor_id": row[4], "language": row[5]} for row in cursor.fetchall()]

    conn.close()
    return doctors

def doctor_panel(username):
    st.title("Doctor Panel")

    # Menu for Doctor Options
    doctor_menu = ["Record new patient visit", "Add New Patient", "View My Info", "View Patient History"]
    choice = st.sidebar.radio("Doctor Options", doctor_menu)

    if choice == "Record new patient visit":     
        if st.button("Check Patient History"):
            patient_username = st.text_input("Patient Username/ID")
            if patient_username:
                patient_history = get_patient_history(patient_username)
                if patient_history:
                    for record in patient_history:
                        st.write(f"Date: {record['date']}, Summary: {record['summary']}")
                else:
                    st.info(f"No medical history found for {patient_name}.")

        st.subheader("Record a New Patient Visit")
        patient_username = st.text_input("Patient User Name")
        summary = st.text_area("Summary")
        
        if st.button("Submit"):
            add_patient_visit(patient_name, summary)
            st.success("Visit recorded successfully!")

    elif choice == "Add New Patient":
        st.subheader("Add a New Patient")
        patient_username = st.text_input("Patient Username")
        patient_password = st.text_input("Patient Password", type="password")
        name = st.text_input("Patient Name")
        date_of_birth = st.date_input("Date of Birth")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        contact_info = st.text_input("Contact Info")
        language = st.text_input("Language")
        
        if st.button("Add Patient"):
            add_patient(patient_username, patient_password, name, date_of_birth, gender, contact_info, language)
            st.success(f"Patient {name} added successfully!")

    elif choice == "View My Info":
        st.subheader("Doctor Info")
        doctor_info = get_doctor_info(username)
        if doctor_info:
            st.write(f"Name: {doctor_info['name']}")
            st.write(f"Username: {doctor_info['username']}")
            st.write(f"Specialization: {doctor_info['specialization']}")
            st.write(f"Contact: {doctor_info['contact_info']}")
            st.write(f"Language: {doctor_info['language']}")
            st.write(f"Doctor ID: {doctor_info['doctor_id']}")
            st.write(f"User ID: {doctor_info['user_id']}")
        else:
            st.info("Doctor info not available.")

    elif choice == "View Patient History":
        st.subheader("Patient History")
        patient_name = st.text_input("Patient Name")
        if patient_name:
            patient_history = get_patient_history(patient_name)
            if patient_history:
                for record in patient_history:
                    st.write(f"Date: {record['date']}, Summary: {record['summary']}")
            else:
                st.info(f"No medical history found for {patient_name}.")
