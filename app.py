import streamlit as st
import matplotlib.pyplot as plt
from db import users_collection, doctors_collection, patients_collection

def login_signup(role):
    st.title(f"{role.capitalize()} Login/Signup")
    option = st.selectbox("Select action", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if option == "Signup":
        if st.button("Create Account"):
            if users_collection.find_one({"username": username}):
                st.write("Username already exists.")
            else:
                users_collection.insert_one({"username": username, "password": password, "role": role})
                st.write("Account created successfully!")
    
    elif option == "Login":
        if st.button("Login"):
            user = users_collection.find_one({"username": username, "password": password, "role": role})
            if user:
                st.session_state['username'] = username
                st.session_state['role'] = role
                st.write("Logged in successfully!")
                if role == 'patient':
                    patient_dashboard()
                elif role == 'doctor':
                    doctor_dashboard()
            else:
                st.write("Invalid credentials.")

def patient_dashboard():
    st.title("Patient Dashboard")
    
    # Show list of doctors
    doctors = doctors_collection.find()
    doctor_options = [doctor['name'] for doctor in doctors]
    selected_doctor_name = st.selectbox("Select a doctor", doctor_options)
    selected_doctor = doctors_collection.find_one({"name": selected_doctor_name})
    
    # Input health data
    name = st.text_input("Patient Name")
    pain_level = st.slider("Menstrual Pain Level (1-10)", 1, 10)
    bleeding_intensity = st.selectbox("Bleeding Intensity", ["Normal", "Heavy", "Very Heavy"])
    missed_periods = st.selectbox("Missed Periods", ["Yes", "No"])
    systolic_bp = st.number_input("Systolic Blood Pressure")
    diastolic_bp = st.number_input("Diastolic Blood Pressure")
    heart_rate = st.number_input("Heart Rate (bpm)")

    # Submit button
    if st.button("Submit"):
        patient_data = {
            "name": name,
            "pain_level": pain_level,
            "bleeding_intensity": bleeding_intensity,
            "missed_periods": missed_periods,
            "systolic_bp": systolic_bp,
            "diastolic_bp": diastolic_bp,
            "heart_rate": heart_rate,
            "doctor_id": selected_doctor['_id']
        }
        patients_collection.insert_one(patient_data)
        
        # Display health data
        st.write("Patient Data:")
        st.write(patient_data)
        
        # Display a graph
        data = {
            "Pain Level": pain_level,
            "Bleeding Intensity": bleeding_intensity,
            "Missed Periods": missed_periods,
            "Systolic BP": systolic_bp,
            "Diastolic BP": diastolic_bp,
            "Heart Rate": heart_rate
        }
        
        fig, ax = plt.subplots()
        ax.bar(data.keys(), data.values())
        st.pyplot(fig)
        
        # Check for alerts
        alerts = []
        if pain_level >= 8:
            alerts.append("Severe menstrual pain.")
        if bleeding_intensity == "Very Heavy":
            alerts.append("Heavy menstrual bleeding.")
        if missed_periods == "Yes":
            alerts.append("Missed periods. Check for pregnancy or hormonal issues.")
        if systolic_bp >= 140 or diastolic_bp >= 90:
            alerts.append("High blood pressure.")
        if heart_rate < 60:
            alerts.append("Low heart rate.")
        elif heart_rate > 100:
            alerts.append("High heart rate.")
        
        if alerts:
            st.write("Alerts:")
            for alert in alerts:
                st.write(alert)
            st.write("Requesting doctor intervention...")
        else:
            st.write("All good.")

def doctor_dashboard():
    st.title("Doctor Dashboard")

    # Ensure session_state has 'username'
    if 'username' not in st.session_state:
        st.write("User not logged in.")
        return

    doctor_name = st.session_state['username']
    doctor = doctors_collection.find_one({"name": doctor_name})
    
    if doctor:
        patients = patients_collection.find({"doctor_id": doctor['_id']})

        if patients.count() > 0:
            st.write("Patient Data:")
            
            for patient in patients:
                st.write("Name: ", patient['name'])
                st.write("Pain Level: ", patient['pain_level'])
                st.write("Bleeding Intensity: ", patient['bleeding_intensity'])
                st.write("Missed Periods: ", patient['missed_periods'])
                st.write("Systolic BP: ", patient['systolic_bp'])
                st.write("Diastolic BP: ", patient['diastolic_bp'])
                st.write("Heart Rate: ", patient['heart_rate'])
                
                # Display a graph for each patient
                data = {
                    "Pain Level": patient['pain_level'],
                    "Bleeding Intensity": patient['bleeding_intensity'],
                    "Missed Periods": patient['missed_periods'],
                    "Systolic BP": patient['systolic_bp'],
                    "Diastolic BP": patient['diastolic_bp'],
                    "Heart Rate": patient['heart_rate']
                }
                
                fig, ax = plt.subplots()
                ax.bar(data.keys(), data.values())
                st.pyplot(fig)
                
                st.write("---")
        else:
            st.write("No patient data available.")

def main():
    if 'role' not in st.session_state:
        st.title("Select User Type")
        role = st.selectbox("Select your role", ["Patient", "Doctor"])
        if st.button("Proceed"):
            st.session_state['role'] = role.lower()
            login_signup(st.session_state['role'])
    else:
        if st.session_state['role'] == 'patient':
            patient_dashboard()
        elif st.session_state['role'] == 'doctor':
            doctor_dashboard()

if __name__ == "__main__":
    main()
