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
    user_input = st.text_input("How can I help you today?")

    if user_input.lower() in ["hi", "hello", "hey"]:
        st.write("Hi! May I know your Patient ID and Name?")
        patient_id = st.text_input("Enter your Patient ID:")
        patient_name = st.text_input("Enter your Full Name:")

        if patient_id and patient_name:
            st.success(f"Thanks {patient_name}, you're now checked in!")
            st.session_state["patient_name"] = patient_name
            st.session_state["patient_id"] = patient_id

    if "book appointment" in user_input.lower():
        if "patient_name" in st.session_state:
            st.write(f"Welcome back, {st.session_state['patient_name']}! Please select your symptoms below:")

            symptoms_list = ["Fever", "Headache", "Cough", "Back Pain", "Skin Rash"]
            selected_symptoms = st.multiselect("Choose your symptoms:", symptoms_list)

            if selected_symptoms:
                st.session_state["symptoms"] = selected_symptoms

                # Recommend General Physician for now
                st.write("Thanks! Based on your symptoms, we recommend seeing a **General Physician** or appropriate specialist.")

                if st.button("Proceed to Book Appointment"):
                    matched_docs = doctors[doctors["Specialty"].str.lower() == "general physician"]

                    if not matched_docs.empty:
                     selected_doctor = st.selectbox("Choose a doctor:", matched_docs["Doctor_Name"].unique())


                        available_times = matched_docs[matched_docs["Doctor Name"] == selected_doctor]["Available Time Slot"].unique()
                        selected_time = st.selectbox("Pick a time slot:", available_times)

                        if st.button("Confirm Appointment"):
                            emergency_name = patients[patients["Patient ID"] == st.session_state["patient_id"]]["Emergency Contact Name"].values[0]

                            st.success(f"✅ Your appointment with **{selected_doctor}** at **{selected_time}** is confirmed!")
                            st.info(f"📢 A reminder has also been sent to your emergency contact: **{emergency_name}**.")
                    else:
                        st.error("No General Physicians found in the system.")
        else:
            st.warning("Please check in first by saying 'hello' and entering your name and ID.")

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
        "Patient ID", "First Name", "Last Name", "Age", "Gender", "No-Shows/Cancellations"
    ]])

