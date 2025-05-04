import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    patients = pd.read_excel("patients.xlsx")
    doctors = pd.read_excel("doctors.xlsx")[["Doctor_ID", "Doctor_Name", "Specialty"]]
    return patients, doctors

patients, doctors = load_data()

# Title
st.title("AVACARE - AI Scheduling Assistant")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Chatbot", "Doctor Availability", "Patient Data"])

# -------------------------------
# Chatbot Page
if page == "Chatbot":
    st.subheader("Chat with AVACARE")
    
    if "patient_registered" not in st.session_state:
        st.session_state.patient_registered = False

    user_input = st.text_input("How can I help you today?")
    
    if not st.session_state.patient_registered and user_input.lower() in ["hello", "hi", "hey"]:
        st.write("Hi! May I know your Patient ID and Name?")
        patient_id = st.text_input("Enter your Patient ID:")
        patient_name = st.text_input("Enter your Full Name:")

        if patient_id and patient_name:
            st.session_state.patient_id = patient_id
            st.session_state.patient_name = patient_name
            st.session_state.patient_registered = True
            st.success(f"Thanks {patient_name}, you're now checked in!")
    
    elif st.session_state.patient_registered:
        user_input = st.text_input("What would you like to do? (e.g. symptoms, book appointment, insurance info)")

        if "symptom" in user_input.lower() or "feel" in user_input.lower():
            symptoms = st.multiselect("Select your symptoms:", ["Headache", "Cough", "Fever", "Back pain", "Fatigue"])
            if symptoms:
                st.write("Thanks! Based on your symptoms, we suggest seeing a General Physician.")
                if st.button("Proceed to Appointment Booking"):
                    st.session_state.trigger_booking = True
        
        elif "insurance" in user_input.lower():
            st.write("We accept most public and private insurance including Medicare, Aetna, Cigna, and UnitedHealthcare.")

        elif "book" in user_input.lower() or "appointment" in user_input.lower():
            st.session_state.trigger_booking = True

        if st.session_state.get("trigger_booking"):
            specialties = doctors["Specialty"].unique()
            selected_specialty = st.selectbox("Select a specialty", specialties)

            filtered_doctors = doctors[doctors["Specialty"] == selected_specialty]
            selected_doctor = st.selectbox("Choose a doctor", filtered_doctors["Doctor Name"].unique())

            available_times = filtered_doctors[filtered_doctors["Doctor Name"] == selected_doctor]["Available Time Slot"].unique()
            selected_time = st.selectbox("Pick a time slot", available_times)

            if st.button("Confirm Appointment"):
                st.success(f"✅ Appointment booked for {st.session_state.patient_name} with **{selected_doctor}** at **{selected_time}**.")
                st.session_state.trigger_booking = False

        elif "bye" in user_input.lower():
            st.write(f"Goodbye {st.session_state.patient_name}, take care!")
            st.session_state.patient_registered = False
            st.session_state.trigger_booking = False

        else:
            st.write("Try saying something like 'I have a headache', 'book appointment', or 'insurance'.")

# -------------------------------
# Doctor Availability Page
# -------------------------------
elif page == "Doctor Availability":
    st.subheader("Doctor Schedule Viewer")
    specialty_filter = st.selectbox("Select Specialty", doctors["Specialty"].dropna().unique())
    filtered_doctors = doctors[doctors["Specialty"] == specialty_filter]
    st.dataframe(filtered_doctors[["Doctor_Name", "Specialty"]])

# -------------------------------
# Patient Data Page
# -------------------------------
elif page == "Patient Data":
    st.subheader("Patient Overview")
    st.write("Explore patient risk profiles and appointments.")
    age_range = st.slider("Filter by Age", min_value=patients["Age"].min(), max_value=patients["Age"].max(), value=(20, 60))
    gender_filter = st.selectbox("Filter by Gender", patients["Gender"].dropna().unique())

    filtered = patients[(patients["Age"] >= age_range[0]) & (patients["Age"] <= age_range[1]) & (patients["Gender"] == gender_filter)]

    st.dataframe(filtered[[
        "Patient_ID", "First_Name", "Last_Name", "Age", "Gender",
        "Symptoms", "Suggested_Specialty", "Risk_Category", "Missed_Appointments",
        "Returning_or_Fresh", "Uber_Voucher_Needed"
    ]])
