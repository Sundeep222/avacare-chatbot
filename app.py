import streamlit as st
import pandas as pd

# Page title
st.title("AVACARE - AI Scheduling Assistant")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Chatbot", "Doctor Availability", "Patient Data"])

@st.cache_data
def load_data():
    patients = pd.read_excel("patients.xlsx")
    doctors = pd.read_excel("doctors.xlsx")
    return patients, doctors

patients, doctors = load_data()

# Session state
if "checked_in" not in st.session_state:
    st.session_state.checked_in = False
if "name" not in st.session_state:
    st.session_state.name = ""
if "specialty" not in st.session_state:
    st.session_state.specialty = ""
if "ready_to_book" not in st.session_state:
    st.session_state.ready_to_book = False

# ---------------- Chatbot ----------------
if page == "Chatbot":
    st.subheader("Chat with AVACARE")
    user_input = st.text_input("How can I help you today?")

    if user_input:
        lower = user_input.lower()

        if not st.session_state.checked_in and any(word in lower for word in ["hi", "hello", "hey"]):
            st.write("Hi! May I know your Patient ID and Name?")
            pid = st.text_input("Enter your Patient ID:")
            pname = st.text_input("Enter your Full Name:")

            if pid and pname:
                st.session_state.checked_in = True
                st.session_state.name = pname
                st.success(f"Thanks {pname}, you're now checked in!")

        elif st.session_state.checked_in and "book" in lower:
            st.write(f"Welcome back, {st.session_state.name}! Please select your symptoms below:")
            symptoms = [
                "Fever", "Cough", "Headache", "Stomach pain", "Rash", "Fatigue", "Shortness of breath", "Ear pain"
            ]
            selected = st.multiselect("Choose your symptoms:", symptoms)

            if selected:
                if any(s in selected for s in ["Cough", "Fever", "Headache"]):
                    specialty = "General Physician"
                elif "Ear pain" in selected:
                    specialty = "ENT Specialist"
                else:
                    specialty = "General Physician"

                st.session_state.specialty = specialty
                st.write(f"Thanks! Based on your symptoms, we recommend seeing a **{specialty}**.")
                if st.button("Proceed to Book Appointment"):
                    st.session_state.ready_to_book = True

        elif st.session_state.ready_to_book:
            docs = doctors[doctors["Specialty"] == st.session_state.specialty]
            if docs.empty:
                st.warning("No doctors available for this specialty.")
            else:
                selected_doc = st.selectbox("Choose a doctor:", docs["Doctor_Name"].unique())
                time = st.selectbox("Pick a time slot:", ["9AM", "11AM", "1PM", "3PM"])
                if st.button("Confirm Appointment"):
                    emergency_name = patients[patients["Full Name"] == st.session_state.name]["Emergency Contact Name"].values[0]
                    st.success(f"✅ Appointment booked with {selected_doc} at {time}!")
                    st.info(f"📲 Emergency contact **{emergency_name}** has been notified.")

        elif not st.session_state.checked_in:
            st.warning("Please check in first by saying hello!")

# ---------------- Doctor Availability ----------------
elif page == "Doctor Availability":
    st.subheader("Doctor Schedule Viewer")
    selected = st.selectbox("Filter by specialty:", doctors["Specialty"].unique())
    df = doctors[doctors["Specialty"] == selected]
    st.dataframe(df[["Doctor_Name", "Specialty", "Years_of_Experience"]])

# ---------------- Patient Data ----------------
elif page == "Patient Data":
    st.subheader("Patient Viewer")
    age_range = st.slider("Age Filter", 18, 80, (20, 60))
    gender = st.selectbox("Gender:", patients["Gender"].unique())
    df = patients[(patients["Age"].between(age_range[0], age_range[1])) & (patients["Gender"] == gender)]
    st.dataframe(df[["Patient ID", "Full Name", "Age", "Gender", "No-Shows", "Emergency Contact Name"]])
