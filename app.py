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
        user_input_lower = user_input.lower()

        # APPOINTMENTS
        if any(word in user_input_lower for word in ["appointment", "book", "schedule"]):
            st.write("You can book an appointment by selecting a time slot with your preferred doctor. Would you like to see who's available?")

        # CANCEL
        elif "cancel" in user_input_lower:
            st.write("No problem. Please provide your name and the appointment date you'd like to cancel.")

        # RESCHEDULE
        elif "reschedule" in user_input_lower or "change time" in user_input_lower:
            st.write("Sure, I can help with that. What day and time would you like to reschedule to?")

        # AVAILABILITY
        elif "available" in user_input_lower or "availability" in user_input_lower or "free" in user_input_lower:
            st.write("Doctors are usually available Monday to Friday from 9 AM to 5 PM. Want to see a full schedule?")

        # SYMPTOMS
        elif "symptom" in user_input_lower or "feel" in user_input_lower or "sick" in user_input_lower:
            st.write("I'm sorry you're not feeling well. Would you like me to recommend a general physician or specialist?")

        # LOCATION
        elif "location" in user_input_lower or "where" in user_input_lower:
            st.write("We’re located at 123 Wellness Way, Suite 100. Need driving directions or parking info?")

        # INSURANCE
        elif "insurance" in user_input_lower or "pay" in user_input_lower or "coverage" in user_input_lower:
            st.write("We accept most public and private insurance. Would you like to see a list of accepted providers?")

        # EMERGENCY
        elif "emergency" in user_input_lower:
            st.write("If this is a medical emergency, please call 911 immediately.")

        # GREETING
        elif any(word in user_input_lower for word in ["hello", "hi", "hey"]):
            st.write("Hi there! I'm AVACARE — your AI scheduling assistant. Ask me about appointments, doctors, or anything else!")

        # THANK YOU / BYE
        elif any(word in user_input_lower for word in ["thanks", "thank you", "bye", "goodbye"]):
            st.write("You're very welcome! Let me know if there's anything else you need.")

     if user_input:
    user_input = user_input.lower()

    if "appointment" in user_input:
        st.write("Sure! Please tell me your preferred doctor or specialty.")
    elif "availability" in user_input:
        st.write("Here are some available slots 👇")
        st.dataframe(doctors)
    elif "data" in user_input:
        st.write("I can check your no-show risk! Please enter your patient ID.")
    elif "insurance" in user_input:
        st.write("We accept most public and private insurance. Would you like to see a list of accepted providers?")
    elif "reschedule" in user_input or "cancel" in user_input:
        st.write("Sure! To reschedule or cancel, please provide your appointment ID or contact us directly at (800) 555-AVACARE.")
    elif "contact" in user_input:
        st.write("Our main clinic line is (800) 555-AVACARE. We’re available Mon–Fri, 8am–5pm.")
    elif "symptom" in user_input:
        st.write("You can describe your symptoms, and I’ll try to help you find the right department!")
    elif "reminder" in user_input:
        st.write("Would you like me to enable SMS or email reminders for upcoming appointments?")
    elif "book" in user_input:
        st.write("To book, please share your preferred date, time, and doctor or specialty.")
    elif "emergency" in user_input:
        st.write("If this is an emergency, please call 911 or go to the nearest hospital immediately.")
    else:
        st.write("I'm still learning. Try asking about appointments or availability!")



# Doctor Availability Page
# Doctor Availability Page
# Doctor Availability Page
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


# Patient Data Page
# Patient Data Page
elif page == "Patient Data":
    st.subheader("Patient No-Show Risk (Simulated Data)")

    # Allow filtering by Age or Gender
    age_filter = st.slider("Filter by Age", min_value=int(patients["Age"].min()), max_value=int(patients["Age"].max()), value=(20, 60))
    gender_filter = st.selectbox("Filter by Gender", options=patients["Gender"].unique())

    filtered_patients = patients[
        (patients["Age"] >= age_filter[0]) & 
        (patients["Age"] <= age_filter[1]) & 
        (patients["Gender"] == gender_filter)
    ]

    st.write("Filtered Patient Records:")
    st.dataframe(filtered_patients[["Unique ID", "First Name", "Last Name", "Age", "Gender", "No-Shows/Cancellations"]])


