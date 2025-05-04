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

    # Initialize session state
    if "patient_registered" not in st.session_state:
        st.session_state.patient_registered = False
        st.session_state.trigger_booking = False
        st.session_state.symptom_shared = False

    # Greeting input
    user_input = st.text_input("How can I help you today?", key="initial_input")

    # Registration step
    if not st.session_state.patient_registered and user_input.lower() in ["hello", "hi", "hey"]:
        st.write("Hi! May I know your Patient ID and Name?")
        patient_id = st.text_input("Enter your Patient ID:")
        patient_name = st.text_input("Enter your Full Name:")

        if patient_id and patient_name:
            st.session_state.patient_id = patient_id
            st.session_state.patient_name = patient_name
            st.session_state.patient_registered = True
            st.success(f"Thanks {patient_name}, you're now checked in!")

    # After registration — continue flow
    elif st.session_state.patient_registered:

        # STEP 1: Symptom Input
        if not st.session_state.symptom_shared:
            st.write(f"Welcome back, {st.session_state.patient_name}! Please select your symptoms below:")
            symptoms = st.multiselect("Choose your symptoms:", ["Headache", "Cough", "Fever", "Back pain", "Fatigue", "Chest pain"])
            if symptoms:
                st.session_state.symptoms = symptoms
                st.session_state.symptom_shared = True
                st.write("Thanks! Based on your symptoms, we recommend seeing a General Physician or appropriate specialist.")
                if st.button("Proceed to Book Appointment"):
                    st.session_state.trigger_booking = True

        # STEP 2: Appointment Booking
        if st.session_state.trigger_booking:
            st.markdown("### Let's get your appointment booked!")

            specialties = doctors["Specialty"].unique()
            selected_specialty = st.selectbox("Select a specialty", specialties)

            filtered_doctors = doctors[doctors["Specialty"] == selected_specialty]
            selected_doctor = st.selectbox("Choose a doctor", filtered_doctors["Doctor Name"].unique())

            available_times = filtered_doctors[filtered_doctors["Doctor Name"] == selected_doctor]["Available Time Slot"].unique()
            selected_time = st.selectbox("Pick a time slot", available_times)

            if st.button("Confirm Appointment"):
                st.success(f"✅ Appointment confirmed for **{st.session_state.patient_name}** with **{selected_doctor}** at **{selected_time}**.")
                # Notify emergency contact
                emergency_name = "Maria Chavez"  # Example contact, can be dynamic
                st.info(f"📢 Notification sent to emergency contact **{emergency_name}** to remind you about your appointment.")
                st.session_state.trigger_booking = False

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
