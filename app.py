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

# Chatbot Page
if page == "Chatbot":
    st.subheader("Chat with AVACARE")
    user_input = st.text_input("Hi! How can I help you today?")

    if user_input:
        if "appointment" in user_input.lower():
            st.write("Sure! Please tell me your preferred doctor or specialty.")
        elif "availability" in user_input.lower():
            st.write("Here are some available slots 👇")
            st.dataframe(doctors[['Doctor', 'Specialty', 'Date', 'Time', 'Available']])
        elif "data" in user_input.lower():
            st.write("I can check your no-show risk! Please enter your patient ID.")
        else:
            st.write("I'm still learning. Try asking about appointments or availability!")

# Doctor Availability Page
elif page == "Doctor Availability":
    st.subheader("Doctor Schedule")
    st.dataframe(doctors)

# Patient Data Page
elif page == "Patient Data":
    st.subheader("Patient No-Show Risk (Simulated Data)")
    st.dataframe(patients[['Unique ID', 'First Name', 'Last Name', 'Age', 'Gender', 'No-Shows/Cancellations']])

