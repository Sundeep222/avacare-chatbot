import streamlit as st
import pandas as pd

# Load data
doctors = pd.read_excel("doctors.xlsx")
patients = pd.read_excel("patients.xlsx")

# Helper function to find patient match
def match_patient(patient_id, full_name):
    matched = patients[(patients['Patient_ID'] == patient_id) &
                       ((patients['First_Name'] + " " + patients['Last_Name']) == full_name)]
    return matched.iloc[0] if not matched.empty else None

# Title
st.title("AVACARE - AI Scheduling Assistant")

# Session state init
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'patient' not in st.session_state:
    st.session_state.patient = None

# Step 0: Chat greeting
prompt = st.text_input("How can I help you today?")
if prompt.lower() in ["hello", "hi"] and st.session_state.step == 0:
    st.session_state.step = 1

# Step 1: Get Patient ID and Name
if st.session_state.step == 1:
    st.subheader("Hi! May I know your Patient ID and Name?")
    patient_id = st.text_input("Enter your Patient ID:")
    full_name = st.text_input("Enter your Full Name:")
    if patient_id and full_name:
        match = match_patient(patient_id, full_name)
        if match is not None:
            st.session_state.patient = match
            st.success(f"Thanks {full_name}, you're now checked in!")
            st.session_state.step = 2
        else:
            st.error("Patient not found. Please check your ID or name.")

# Step 2: Booking symptoms
if st.session_state.step == 2 and prompt.lower() == "book appointment":
    st.write(f"Welcome back, {st.session_state.patient['First_Name']} {st.session_state.patient['Last_Name']}! Please select your symptoms below:")
    symptoms = st.multiselect("Choose your symptoms:", ["Headache", "Fever", "Cough", "Stomach pain"])
    if symptoms:
        specialty = "General Physician"  # Can be logic-driven in future
        st.write(f"Thanks! Based on your symptoms, we recommend seeing a **{specialty}**.")
        if st.button("Proceed to Book Appointment"):
            st.session_state.step = 3
            st.session_state.specialty = specialty

# Step 3: Choose doctor and time
if st.session_state.step == 3:
    matched_docs = doctors[doctors["Specialty"] == st.session_state.specialty]
    if not matched_docs.empty:
        selected_doctor = st.selectbox("Choose a doctor:", matched_docs["Doctor_Name"])
        selected_time = st.selectbox("Choose a time slot:", ["9 AM - 10 AM", "10 AM - 11 AM", "11 AM - 12 PM"])
        if st.button("Confirm Appointment"):
            patient_name = st.session_state.patient['First_Name'] + " " + st.session_state.patient['Last_Name']
            emergency_name = st.session_state.patient['Emergency_Contact_Name']
            patient_email = st.session_state.patient["Email"]
            appointment_date = "2025-05-06"

            st.session_state.step = 4

            # Confirmation message
            st.markdown(f"""
            ✅ **Appointment Confirmed!**  
            **Patient:** {patient_name}  
            **Doctor:** {selected_doctor}  
            **Date & Time:** {appointment_date} at {selected_time}  
            **Location:** Dallas  
            **Insurance:** {st.session_state.patient['Insurance_Type']}  

            📩 A reminder will also be sent shortly to your emergency contact: **{emergency_name}**  

            Thank you, **{patient_name}**. See you soon! 😊
            """)
# Ask if they want a simulated email reminder
# Save confirmation flag to session state
st.session_state.appointment_confirmed = True

# Show reminder options only if appointment was confirmed
if 'appointment_confirmed' not in st.session_state:
    st.session_state.appointment_confirmed = False

if st.session_state.appointment_confirmed:
    st.write("Would you like to receive a reminder confirmation?")
    send_reminder = st.radio("Send simulated email reminder?", ["Yes", "No"], key="reminder_choice")

    if send_reminder == "Yes":
        if st.button("Simulate Email Reminder"):
            st.success("📨 Email reminder simulated successfully!")
            st.info("👋 Goodbye! Talk to you soon 😊")
    else:
        st.info("👋 Okay! Your appointment is confirmed. Talk to you soon 😊")



# Sidebar
st.sidebar.title("Navigation")
st.sidebar.radio("Go to", ["Chatbot", "Doctor Availability", "Patient Data"])

