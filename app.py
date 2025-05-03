import streamlit as st
import pandas as pd

# Title
st.title("AVACARE - AI Scheduling Assistant")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Chatbot", "Doctor Availability", "Patient Data"])

# Load data
@st.cache_data
def load_data():
    patients = pd.read_excel("patients.xlsx")
    doctors = pd.read_excel("doctors.xlsx")
    return patients, doctors

patients, doctors = load_data()

# ------------------------------
# Chatbot Page
# ------------------------------
if page == "Chatbot":
    st.subheader("Chat with AVACARE")
    if "symptom_specialty" not in st.session_state:
        st.session_state.symptom_specialty = None

    user_input = st.text_input("Hi! How can I help you today?")

    if user_input:
        user_input_lower = user_input.lower()

        # --- SYMPTOM MATCH ---
        symptoms_map = {
            "headache": "General Physician",
            "stomach": "Gastroenterologist",
            "skin": "Dermatologist",
            "anxiety": "Psychiatrist",
            "cough": "Pulmonologist"
        }

        matched_symptom = next((symptom for symptom in symptoms_map if symptom in user_input_lower), None)
        if matched_symptom:
            specialty = symptoms_map[matched_symptom]
            st.session_state.symptom_specialty = specialty
            st.write(f"Based on your symptoms, you might want to see a **{specialty}**. Would you like to proceed with booking?")

        # --- YES BOOK FROM SYMPTOM ---
        elif user_input_lower.strip() == "yes" and st.session_state.symptom_specialty:
            specialty = st.session_state.symptom_specialty
            st.write(f"Let's get you booked with a **{specialty}**!")

            filtered_doctors = doctors[doctors["Specialty"] == specialty]
            selected_doctor = st.selectbox("Choose a doctor", filtered_doctors["Doctor Name"].unique())
            available_times = filtered_doctors[filtered_doctors["Doctor Name"] == selected_doctor]["Available Time Slot"].unique()
            selected_time = st.selectbox("Pick a time slot", available_times)

            if st.button("Confirm Appointment"):
                st.success(f"✅ Your appointment with **{selected_doctor}** at **{selected_time}** is confirmed!")
                st.session_state.symptom_specialty = None  # reset intent

        # --- BOOKING INTENT ---
        elif any(word in user_input_lower for word in ["appointment", "book", "schedule"]):
            st.write("Let's help you book an appointment!")
            specialties = doctors["Specialty"].unique()
            selected_specialty = st.selectbox("Select a specialty", specialties)

            filtered_doctors = doctors[doctors["Specialty"] == selected_specialty]
            selected_doctor = st.selectbox("Choose a doctor", filtered_doctors["Doctor Name"].unique())
            available_times = filtered_doctors[filtered_doctors["Doctor Name"] == selected_doctor]["Available Time Slot"].unique()
            selected_time = st.selectbox("Pick a time slot", available_times)

            if st.button("Confirm Appointment"):
                st.success(f"✅ Your appointment with **{selected_doctor}** at **{selected_time}** is confirmed!")

        # Other intents (cancel, insurance, etc.) come here

# ------------------------------
# Doctor Availability Page
# ------------------------------
elif page == "Doctor Availability":
    st.subheader("Doctor Schedule Viewer")

    selected_specialty = st.selectbox("Filter by specialty:", options=doctors["Specialty"].unique())
    filtered = doctors[doctors["Specialty"] == selected_specialty]

    st.write(f"Showing availability for **{selected_specialty}**:")
    st.dataframe(filtered[[
        "Doctor Name", 
        "Available Days", 
        "Available Time Slot", 
        "Slot Duration (mins)", 
        "Approx. Slots Per Day", 
        "Booking Status"
    ]])

    if st.button("Show All Doctors"):
        st.dataframe(doctors)

# ------------------------------
# Patient Data Page
# ------------------------------
elif page == "Patient Data":
    st.subheader("Patient No-Show Risk (Simulated Data)")

    age_filter = st.slider("Filter by Age", min_value=int(patients["Age"].min()), max_value=int(patients["Age"].max()), value=(20, 60))
    gender_filter = st.selectbox("Filter by Gender", options=patients["Gender"].unique())

    filtered_patients = patients[
        (patients["Age"] >= age_filter[0]) & 
        (patients["Age"] <= age_filter[1]) & 
        (patients["Gender"] == gender_filter)
    ]

    st.write("Filtered Patient Records:")
    st.dataframe(filtered_patients[[
        "Unique ID", "First Name", "Last Name", "Age", "Gender", "No-Shows/Cancellations"
    ]])
