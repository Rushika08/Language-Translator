import streamlit as st
from user_functions import login, admin_panel, create_admin_in_db, hash_password, check_admin_exists
from doctor_functions import doctor_panel,add_doctor
from patient_functions import add_patient
from healthcare_db import create_tables

# Initialize database
# create_tables()

# Streamlit UI
st.title("Healthcare Management System")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None

# Logout function
def logout_user():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.sidebar.success("Logged out successfully.")

# Sidebar Menu
if st.session_state.logged_in:
    st.sidebar.success(f"Logged in as {st.session_state.role}: {st.session_state.username}")
    st.sidebar.button("Logout", on_click=logout_user)
else:
    menu = ["Admin Login", "Doctor Login", "Patient Login"]
    choice = st.sidebar.selectbox("Select Login Option", menu)

    if choice == "Admin Login":
        st.subheader("Admin Login")
        username = st.text_input("Admin Username")
        password = st.text_input("Admin Password", type="password")
        if st.button("Login"):
            user = login(username, password)
            if user and user[1] == "Admin":
                st.success(f"Logged in as Admin: {username}")
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.session_state.username = username
            else:
                st.error("Invalid Admin credentials")

    elif choice == "Doctor Login":
        st.subheader("Doctor Login")
        username = st.text_input("Doctor Username")
        password = st.text_input("Doctor Password", type="password")
        if st.button("Login"):
            user = login(username, password)
            if user and user[1] == "Doctor":
                st.success(f"Logged in as Doctor: {username}")
                st.session_state.logged_in = True
                st.session_state.role = "Doctor"
                st.session_state.username = username
            else:
                st.error("Invalid Doctor credentials")

    elif choice == "Patient Login":
        st.subheader("Patient Login")
        username = st.text_input("Patient Username")
        password = st.text_input("Patient Password", type="password")
        if st.button("Login"):
            user = login(username, password)
            if user and user[1] == "Patient":
                st.success(f"Logged in as Patient: {username}")
                st.session_state.logged_in = True
                st.session_state.role = "Patient"
                st.session_state.username = username
            else:
                st.error("Invalid Patient credentials")

# Role-Specific Panels
if st.session_state.logged_in:
    if st.session_state.role == "Admin":
        admin_panel()
    elif st.session_state.role == "Doctor":
        st.subheader("Doctor Panel")
        doctor_panel(st.session_state.username)
        # st.info("Add a new patient")
        # patient_username = st.text_input("Patient Username")
        # patient_password = st.text_input("Patient Password", type="password")
        # patient_name = st.text_input("Patient Name")
        # patient_dob = st.date_input("Patient Date of Birth")
        # patient_gender = st.selectbox("Patient Gender", ["Male", "Female", "Other"])
        # patient_contact = st.text_input("Patient Contact Info")
        # patient_language = st.text_input("Patient Language")
        # if st.button("Add Patient"):
        #     if all([patient_username, patient_password, patient_name, patient_contact, patient_language]):
        #         add_patient(patient_username, patient_password, patient_name, patient_dob, patient_gender, patient_contact, patient_language)
        #         st.success(f"Patient {patient_name} added successfully!")
        #     else:
        #         st.error("Please fill in all required fields.")

    elif st.session_state.role == "Patient":
        st.subheader("Patient Panel")
        st.info("View your medical history")
        # Add functionality for viewing medical history here
