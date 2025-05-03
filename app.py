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
    user_input = st.text_input("Hi! How can I help you today?")

    if user_input:
        user_input_lower = user_input.lower()

        # Appointment Booking
        if any(word in user_input_lower for word in ["appointment", "book", "schedule"]):
            specialties = doctors["Specialty"].unique()
            st.write("Let's help you book an appointment!")
            selected_specialty = st.selectbox("Select a specialty", specialties)

            filtered_doctors = doctors[doctors["Specialty"] == selected_specialty]
            selected_doctor = st.selectbox("Choose a doctor", filtered_doctors["Doctor Name"].unique())

            available_times = filtered_doctors[filtered_doctors["Doctor Name"] == selected_doctor]["Available Time Slot"].unique()
            selected_time = st.selectbox("Pick a time slot", available_times)

            if st.button("Confirm Appointment"):
                st.success(f"✅ Your appointment with **{selected_doctor}** at **{selected_time}** is confirmed!")

        # Cancel
        elif "cancel" in user_input_lower:
            st.write("No problem. Please provide your name and the appointment date you'd like to cancel.")

        # Reschedule
        elif "reschedule" in user_input_lower or "change time" in user_input_lower:
            st.write("Sure, I can help with that. What day and time would you like to reschedule to?")

        # Availability
        elif "available" in user_input_lower or "availability" in user_input_lower or "free" in user_input_lower:
            st.write("Doctors are usually available Monday to Friday from 9 AM to 5 PM. Want to see a full schedule?")

        # Symptoms
        elif any(symptom in user_input_lower for symptom in ["headache", "fever", "cough", "nausea", "sore throat", "sick"]):
            st.write("Based on your symptoms, you might want to see a General Physician or relevant specialist. Would you like to proceed with booking?")

        # Health Tips
        elif "tip" in user_input_lower or "advice" in user_input_lower:
            st.write("💡 Health Tip: Stay hydrated, get at least 7-8 hours of sleep, and exercise regularly to boost your immunity.")

        # Insurance
        elif any(word in user_input_lower for word in ["insurance", "pay", "coverage", "aetna", "medicaid", "unitedhealth"]):
            if any(provider in user_input_lower for provider in ["aetna", "united", "medicaid"]):
                st.write("✅ Yes, we accept your insurance provider!")
            else:
                st.write("We accept most public and private insurance. Please provide your plan name if you'd like us to verify.")

        # Location
        elif "location" in user_input_lower or "where" in user_input_lower:
            st.write("We’re located at 123 Wellness Way, Suite 100. Need driving directions or parking info?")

        # Emergency
        elif "emergency" in user_input_lower:
            st.write("If this is a medical emergency, please call 911 immediately.")

        # Greeting
        elif any(word in user_input_lower for word in ["hello", "hi", "hey"]):
            st.write("Hi there! I'm AVACARE — your AI scheduling assistant. Ask me about appointments, doctors, or anything else!")

        # Thanks / Bye
        elif any(word in user_input_lower for word in ["thanks", "thank you", "bye", "goodbye"]):
            st.write("You're very welcome! Let me know if there's anything else you need.")

        # Fallback
        else:
            st.write("I'm still learning. Try asking about appointments, symptoms, insurance, or availability!")

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

    # Filter by Age and Gender
    age_filter = st.slider("Filter by Age", min_value=int(patients["Age"].min()), max_value=int(patients["Age"].max()), value=(20, 60))
    gender_filter = st.selectbox("Filter by Gender", options=patients["Gender"].unique())

    filtered_patients = patients[
        (patients["Age"] >= age_filter[0]) & 
        (patients["Age"] <= age_filter[1]) & 
        (patients["Gender"] == gender_filter)
    ]

    st.write("Filtered Patient Records:")
    st.dataframe(filtered_patients[
        ["Unique ID", "First Name", "Last Name", "Age", "Gender", "No-Shows/Cancellations"]
    ])
