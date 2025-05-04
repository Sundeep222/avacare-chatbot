import streamlit as st
import pandas as pd

# Title
st.title("AVACARE - AI Scheduling Assistant")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Chatbot", "Doctor Availability", "Patient Data"])

# Load data
@st.cache_data
def load_data():
    patients = pd.read_excel("patients.xlsx")
    doctors = pd.read_excel("doctors.xlsx")
    return patients, doctors

patients, doctors = load_data()

def match_patient(patient_id, full_name):
    first, last = full_name.strip().split(" ", 1)  # splits "James Chavez" into "James", "Chavez"
    matched = patients[
        (patients['Patient_ID'] == patient_id) &
        (patients['First_Name'].str.lower() == first.lower()) &
        (patients['Last_Name'].str.lower() == last.lower())
    ]
    return matched


# ----------------------------
# Chatbot Page
# ----------------------------
if page == "Chatbot":
    st.subheader("Chat with AVACARE")
    user_input = st.text_input("How can I help you today?")

    if user_input:
        user_input = user_input.lower()

        if any(word in user_input for word in ["hello", "hi", "hey"]):
            st.write("Hi! May I know your Patient ID and Name?")
            patient_id = st.text_input("Enter your Patient ID:")
            full_name = st.text_input("Enter your Full Name:")

            if patient_id and full_name:
                match = match_patient(patient_id, full_name)
                if not match.empty:
                    st.success(f"Thanks {full_name}, you're now checked in!")
                    st.session_state['patient_name'] = full_name
                    st.session_state['patient_id'] = patient_id
                else:
                    st.error("Sorry, we couldn’t find your record.")

        elif "book appointment" in user_input:
            if 'patient_name' not in st.session_state:
                st.warning("Please say 'hello' first to check in.")
            else:
                name = st.session_state['patient_name']
                st.write(f"Welcome back, {name}! Please select your symptoms below:")
                symptoms = st.multiselect("Choose your symptoms:", ["Fever", "Cough", "Stomach pain", "Headache", "Skin rash"])

                if symptoms:
                    st.write("Thanks! Based on your symptoms, we recommend seeing a **General Physician** or appropriate specialist.")

                    if st.button("Proceed to Book Appointment"):
                        specialty = "General Physician"
                        matched_docs = doctors[doctors["Specialty"] == specialty]

                        if not matched_docs.empty:
                            selected_doctor = st.selectbox("Choose a doctor:", matched_docs["Doctor_Name"])
                            time_slots = ["9 AM - 10 AM", "11 AM - 12 PM", "2 PM - 3 PM", "4 PM - 5 PM"]
                            selected_time = st.selectbox("Choose a time slot:", time_slots)

                            if st.button("Confirm Appointment"):
                                emergency_contact = patients.loc[patients['Patient_ID'] == st.session_state['patient_id'], 'Emergency_Contact_Name'].values[0]
                                st.success(f"✅ Appointment booked with {selected_doctor} at {selected_time}.")
                                st.info(f"📲 A reminder has been sent to your emergency contact: {emergency_contact}.")
                        else:
                            st.error("Sorry, no doctors found for that specialty.")

        else:
            st.write("Try saying 'hello' or 'book appointment'.")

# ----------------------------
# Doctor Availability Page
# ----------------------------
elif page == "Doctor Availability":
    st.subheader("Doctor Schedule Viewer")
    specialty = st.selectbox("Choose a specialty:", doctors["Specialty"].unique())
    st.dataframe(doctors[doctors["Specialty"] == specialty])

# ----------------------------
# Patient Data Page
# ----------------------------
elif page == "Patient Data":
    st.subheader("Patient Records Viewer")
    st.dataframe(patients)

    df = patients[(patients["Age"].between(age_range[0], age_range[1])) & (patients["Gender"] == gender)]
    st.dataframe(df[["Patient ID", "Full Name", "Age", "Gender", "No-Shows", "Emergency Contact Name"]])

st.success(f"""
✅ **Appointment Confirmed!**

Thank you, **{patient_name}**. Your appointment details are below:

- **Doctor:** {doctor_name} ({specialty})  
- **Date:** {appointment_date}  
- **Time:** {appointment_time}  

📢 A reminder has been sent to your emergency contact: **{emergency_contact}**.  

👋 See you soon! Stay well, and don’t forget to arrive a few minutes early.
""")
