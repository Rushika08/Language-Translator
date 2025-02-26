from healthcare_db import get_connection
from patient_functions import get_patient_history, add_patient, add_patient_visit
from recording_page import recognize_speech, translate_and_speak, summarize_conversation
import streamlit as st
from audio_recorder_streamlit import audio_recorder


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
    doctor_menu = ["Record new patient visit", "Conversation Assistant", "Add New Patient", "View My Info", "View Patient History"]
    choice = st.sidebar.radio("Doctor Options", doctor_menu)

    if choice == "Record new patient visit":     
        # if st.button("Check Patient History"):
        #     patient_username = st.text_input("Patient Username/ID")
        #     # if patient_username:
        #     if st.button("Submit"):
        #         st.write("Hi")
        #         patient_history = get_patient_history(patient_username)
        #         if patient_history:
        #             for record in patient_history:
        #                 st.write(f"Date: {record['date']}, Summary: {record['summary']}")
        #         else:
        #             st.info(f"No medical history found for {patient_name}.")

        # st.subheader("Record a New Patient Visit")
        # patient_username = st.text_input("Patient User Name")
        # summary = st.text_area("Summary")
        
        # # if st.button("Submit"):
        # #     add_patient_visit(patient_name, summary)
        # #     st.success("Visit recorded successfully!")
        st.subheader("Check Patient History")

        patient_username = st.text_input("Enter Patient Username/ID")  # Input should be defined before the button
        
        if st.button("Check History"):
            if patient_username:  # Ensure a username is entered
                patient_history = get_patient_history(patient_username)
                
                if patient_history:
                    st.subheader(f"Medical History for {patient_username}")
                    for record in patient_history:
                        st.write(f"📅 Date: {record['date']}")
                        st.write(f"📝 Summary: {record['summary']}")
                        st.write("---")  # Separator for readability
                else:
                    st.info(f"No medical history found for {patient_username}.")
            else:
                st.warning("Please enter a patient username before checking history.")

        st.subheader("Record a New Patient Visit")
        
        patient_username = st.text_input("Patient User Name")
        summary = st.text_area("Summary")
        
        if st.button("Submit Visit"):
            if patient_username and summary:
                add_patient_visit(51, patient_username, summary)
                st.success(f"Visit recorded successfully for {patient_username}!")
            else:
                st.warning("Please enter both patient username and summary.")
    
    elif choice == "Conversation Assistant":
        st.subheader("Doctor-Patient Conversation Assistant")
        
        # Language selection
        st.subheader("Select Language Preferences")
        doctor_lang = st.selectbox("Doctor's Language", ["en", "si", "ta", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh-CN"])
        patient_lang = st.selectbox("Patient's Language", ["si", "en", "ta", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh-CN"])

        # Role selection
        role = st.radio("Select Your Role", ["Doctor", "Patient"])
        st.write(f"**{role} Role Selected**")

        # Audio Recording
        st.subheader("Record Your Speech")
        audio_bytes = audio_recorder()

        if "conversation" not in st.session_state:
            st.session_state.conversation = []

        if audio_bytes:
            # Recognize speech based on selected role
            language = doctor_lang if role == "Doctor" else patient_lang
            recognized_text = recognize_speech(language, audio_bytes)

            # If speech was recognized, translate and generate speech
            if recognized_text:
                dest_lang = patient_lang if role == "Doctor" else doctor_lang
                src_lang = doctor_lang if role == "Doctor" else patient_lang

                translated_text, translated_audio = translate_and_speak(recognized_text, dest_lang, src_lang)
                
                # Play translated speech
                if translated_audio:
                    st.audio(translated_audio, format="audio/mp3")

                if translated_text:
                    st.write(f"**Recognized Text ({language}):** {recognized_text}")
                    st.write(f"**Translated Text ({dest_lang}):** {translated_text}")
                    
                    if st.button("Append to Conversation"):
                        if role == "Doctor":
                            st.session_state.conversation.append(f"Doctor: {recognized_text}")
                        else:
                            st.session_state.conversation.append(f"Patient: {translated_text}")

        # Display conversation history
        if st.session_state.conversation:
            st.subheader("Conversation History")
            for entry in st.session_state.conversation:
                st.write(entry)

        # Button to summarize conversation
        if st.button("Summarize Conversation") and st.session_state.conversation:
            summarize_conversation(st.session_state.conversation)

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
