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
# -------------------------------
if page == "Chatbot":
    st.subheader("Chat with AVACARE")
    if "patient_id" not in st.session_state:
        st.session_state.patient_id = None
    if "patient_name" not in st.session_state:
        st.session_state.patient_name = None
    if "specialty_context" not in st.session_state:
        st.session_state.specialty_context = None

    user_input = st.text_input("How can I help you today?")

    if user_input:
        user_input_lower = user_input.lower()

        # Greet + Ask for Patient ID
        if any(word in user_input_lower for word in ["hi", "hello", "hey"]):
            st.write("Hi! May I know your Patient ID and Name?")
            st.session_state.patient_id = st.text_input("Enter your Patient ID:", key="pid")
            st.session_state.patient_name = st.text_input("Enter your Full Name:", key="pname")

        elif st.session_state.patient_id and st.session_state.patient_name:
            # SYMPTOMS to SPECIALIST mapping
            symptom_map = {
                "headache": "General Physician",
                "fatigue": "General Physician",
                "fever": "General Physician",
                "cough": "ENT Specialist",
                "pain": "Orthopedist",
                "eczema": "Dermatology",
                "rash": "Dermatology",
                "insomnia": "Psychologist",
                "depression": "Psychologist",
            }

            matched_specialty = None
            for symptom, specialty in symptom_map.items():
                if symptom in user_input_lower:
                    matched_specialty = specialty
                    break

            if matched_specialty:
                st.session_state.specialty_context = matched_specialty
                st.write(f"Based on your symptom, we suggest booking with a **{matched_specialty}**. Proceed below:")

                matched_doctors = doctors[doctors["Specialty"] == matched_specialty]
                if not matched_doctors.empty:
                    selected_doctor = st.selectbox("Choose a doctor:", matched_doctors["Doctor_Name"].unique())
                    selected_date = st.date_input("Select appointment date")
                    selected_time = st.selectbox("Pick a time slot:", ["9:00 AM", "11:00 AM", "1:00 PM", "3:00 PM"])
                    if st.button("Confirm Appointment"):
                        st.success(f"✅ Appointment confirmed with **{selected_doctor}** on **{selected_date}** at **{selected_time}**.")
                        st.session_state.specialty_context = None
                else:
                    st.warning("No doctors found for that specialty right now.")

            elif "insurance" in user_input_lower:
                st.write("We accept Aetna, BlueCross, Medicaid, Medicare, UnitedHealth, and more.")

            elif "tips" in user_input_lower or "advice" in user_input_lower:
                st.write("💡 Health Tip: Stay hydrated, sleep 7–8 hours, and walk 20 mins a day!")

            elif "uber" in user_input_lower or "voucher" in user_input_lower:
                pid = st.session_state.patient_id
                patient_row = patients[patients["Patient_ID"] == pid]
                if not patient_row.empty and patient_row.iloc[0]["Uber_Voucher_Needed"] == "Yes":
                    st.write("✅ You're eligible for an Uber health voucher. We will send it via text before your visit.")
                else:
                    st.write("You're currently not marked as needing a voucher, but you may still request assistance at the front desk.")

            elif "emergency" in user_input_lower:
                st.write("⚠️ If this is a medical emergency, please call 911 or go to your nearest hospital.")

            else:
                st.write("I'm still learning. Try asking about symptoms, insurance, Uber help, or booking.")

        else:
            st.warning("Please enter your Patient ID and Name to continue.")

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
