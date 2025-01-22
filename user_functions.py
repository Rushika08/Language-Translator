import bcrypt
from healthcare_db import get_connection
import streamlit as st
from doctor_functions import add_doctor, get_all_doctors
from patient_functions import get_all_patients

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
    # return bcrypt.hashpw(password, salt)

def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    print(username)
    print(password)
    # Fetch the hashed password and role for the user
    cursor.execute("""
        SELECT username, password, role FROM users WHERE username = ?
    """, (username,))
    user = cursor.fetchone()
    print(user)
    conn.close()
    
    stored_username = user[0]
    hashed_password = user[1]
    role = user[2]

    print(stored_username)
    print(hashed_password)
    

    if user:
        stored_username = user[0]
        hashed_password = user[1]
        role = user[2]
        # Ensure hashed_password is used directly
        # encoded_password = password.encode('utf-8')
        # if bcrypt.checkpw(encoded_password, hashed_password):
        if password == hashed_password:
            print(f"Login successful. Welcome, {stored_username}!")
            return (stored_username, role)  # Return username and role
        else:
            print("Invalid password.")
            return None
    else:
        print("Invalid username.")
        return None


# Function to create admin user in the database
def create_admin_in_db(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    # # Check if the admin already exists
    # cursor.execute('SELECT * FROM Users WHERE role = "Admin" LIMIT 1')
    # admin_exists = cursor.fetchone()

    # if not admin_exists:
    cursor.execute('''
    INSERT INTO Users (username, password, role)
    VALUES (?, ?, ?)
    ''', (username, password, 'Admin'))
    conn.commit()
    print("Admin user created successfully.")
    # else:
    #     print("Admin user already exists.")
    
    conn.close()


def check_admin_exists():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Users WHERE role = "Admin" LIMIT 1')
    admin_exists = cursor.fetchone()

    conn.close()

    return admin_exists is not None

def get_all_admins():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username 
        FROM users 
        WHERE role = 'Admin'
    """)
    admins = [{"username": row[0]} for row in cursor.fetchall()]

    conn.close()
    return admins

# Admin Panel
def admin_panel():
    st.title("Admin Panel")
    
    # Menu for Admin Options
    admin_menu = ["Add New Doctor", "View All Doctors", "View All Patients", "View All Admins"]
    choice = st.sidebar.radio("Admin Options", admin_menu)

    if choice == "Add New Doctor":
        st.subheader("Add a New Doctor")
        doctor_username = st.text_input("Doctor Username")
        doctor_password = st.text_input("Doctor Password", type="password")
        name = st.text_input("Name")
        specialization = st.text_input("Specialization")
        contact_info = st.text_input("Contact Info")
        language = st.text_input("Language")
        
        if st.button("Add Doctor"):
            add_doctor(doctor_username, doctor_password, name, specialization, contact_info, language)
            st.success(f"Doctor {name} added successfully!")

    elif choice == "View All Doctors":
        st.subheader("List of All Doctors")
        doctors = get_all_doctors()
        if doctors:
            for doctor in doctors:
                st.write(f"Name: {doctor['name']}, Specialization: {doctor['specialization']}, Contact: {doctor['contact_info']}")
        else:
            st.info("No doctors found.")

    elif choice == "View All Patients":
        st.subheader("List of All Patients")
        patients = get_all_patients()
        if patients:
            for patient in patients:
                st.write(f"Name: {patient['name']}, Contact: {patient['contact_info']}, Gender: {patient['gender']}")
        else:
            st.info("No patients found.")

    elif choice == "View All Admins":
        st.subheader("List of All Admins")
        admins = get_all_admins()
        if admins:
            for admin in admins:
                st.write(f"Username: {admin['username']}")
        else:
            st.info("No admins found.")

