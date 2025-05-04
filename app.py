import streamlit as st
import pandas as pd

# Load data
doctors = pd.read_excel("doctors.xlsx")
patients = pd.read_excel("patients.xlsx")

# Translation dictionary
translations = {
    "English": {
        "greet": "How can I help you today?",
        "patient_prompt": "Hi! May I know your Patient ID and Name?",
        "enter_id": "Enter your Patient ID:",
        "enter_name": "Enter your Full Name:",
        "checked_in": "Thanks {}, you're now checked in!",
        "not_found": "Patient not found. Please check your ID or name.",
        "symptom_greet": "Welcome back, {}! Please select your symptoms below:",
        "choose_symptoms": "Choose your symptoms:",
        "recommend": "Thanks! Based on your symptoms, we recommend seeing a **{}**.",
        "proceed_btn": "Proceed to Book Appointment",
        "choose_doctor": "Choose a doctor:",
        "choose_time": "Choose a time slot:",
        "confirm_btn": "Confirm Appointment",
        "confirmation": "✅ **Appointment Confirmed!**",
        "patient": "**Patient:**",
        "doctor": "**Doctor:**",
        "datetime": "**Date & Time:**",
        "location": "**Location:** Dallas",
        "insurance": "**Insurance:**",
        "reminder": "📩 A reminder will also be sent shortly to your emergency contact: **{}**",
        "bye": "Thank you, **{}**. See you soon! 😊",
        "ask_reminder": "Would you like to receive a reminder confirmation?",
        "radio_reminder": "Send simulated email reminder?",
        "reminder_success": "📨 Email reminder simulated successfully!",
        "reminder_bye": "👋 Goodbye! Talk to you soon 😊",
        "reminder_skip": "👋 Okay! Your appointment is confirmed. Talk to you soon 😊"
    },
    "Spanish": {
        "greet": "¿Cómo puedo ayudarte hoy?",
        "patient_prompt": "¡Hola! ¿Puedo conocer su ID de paciente y nombre?",
        "enter_id": "Ingrese su ID de paciente:",
        "enter_name": "Ingrese su nombre completo:",
        "checked_in": "Gracias {}, ¡ya estás registrado!",
        "not_found": "Paciente no encontrado. Por favor verifica tu ID o nombre.",
        "symptom_greet": "¡Bienvenido de nuevo, {}! Por favor seleccione sus síntomas a continuación:",
        "choose_symptoms": "Elija sus síntomas:",
        "recommend": "¡Gracias! Según sus síntomas, recomendamos ver a un **{}**.",
        "proceed_btn": "Proceder a reservar cita",
        "choose_doctor": "Elija un médico:",
        "choose_time": "Elija un horario:",
        "confirm_btn": "Confirmar cita",
        "confirmation": "✅ **¡Cita confirmada!**",
        "patient": "**Paciente:**",
        "doctor": "**Médico:**",
        "datetime": "**Fecha y hora:**",
        "location": "**Ubicación:** Dallas",
        "insurance": "**Seguro:**",
        "reminder": "📩 Se enviará un recordatorio pronto a su contacto de emergencia: **{}**",
        "bye": "Gracias, **{}**. ¡Nos vemos pronto! 😊",
        "ask_reminder": "¿Desea recibir una confirmación de recordatorio?",
        "radio_reminder": "¿Enviar recordatorio simulado por correo electrónico?",
        "reminder_success": "📨 ¡Recordatorio de correo electrónico simulado con éxito!",
        "reminder_bye": "👋 ¡Adiós! Hablamos pronto 😊",
        "reminder_skip": "👋 Está bien. Su cita está confirmada. Hablamos pronto 😊"
    },
    "Hindi": {
        "greet": "मैं आपकी कैसे मदद कर सकता हूँ?",
        "patient_prompt": "नमस्ते! कृपया अपना रोगी आईडी और नाम बताएं?",
        "enter_id": "अपना रोगी आईडी दर्ज करें:",
        "enter_name": "अपना पूरा नाम दर्ज करें:",
        "checked_in": "धन्यवाद {}, आप सफलतापूर्वक चेक-इन हो गए हैं!",
        "not_found": "रोगी नहीं मिला। कृपया ID या नाम जांचें।",
        "symptom_greet": "वापसी पर स्वागत है, {}! कृपया नीचे अपने लक्षण चुनें:",
        "choose_symptoms": "अपने लक्षण चुनें:",
        "recommend": "धन्यवाद! आपके लक्षणों के आधार पर हम सलाह देते हैं कि आप **{}** से मिलें।",
        "proceed_btn": "नियुक्ति बुक करने के लिए आगे बढ़ें",
        "choose_doctor": "डॉक्टर चुनें:",
        "choose_time": "समय स्लॉट चुनें:",
        "confirm_btn": "नियुक्ति की पुष्टि करें",
        "confirmation": "✅ **नियुक्ति की पुष्टि हो गई!**",
        "patient": "**रोगी:**",
        "doctor": "**डॉक्टर:**",
        "datetime": "**तारीख और समय:**",
        "location": "**स्थान:** Dallas",
        "insurance": "**बीमा:**",
        "reminder": "📩 एक रिमाइंडर जल्द ही आपके आपातकालीन संपर्क को भेजा जाएगा: **{}**",
        "bye": "धन्यवाद, **{}**। जल्द मिलते हैं! 😊",
        "ask_reminder": "क्या आप एक रिमाइंडर प्राप्त करना चाहेंगे?",
        "radio_reminder": "क्या नकली ईमेल रिमाइंडर भेजें?",
        "reminder_success": "📨 नकली ईमेल रिमाइंडर सफलतापूर्वक भेजा गया!",
        "reminder_bye": "👋 अलविदा! जल्द बात करते हैं 😊",
        "reminder_skip": "👋 ठीक है! आपकी नियुक्ति की पुष्टि हो गई है। जल्द मिलते हैं 😊"
    }
}

# Language selector
language = st.selectbox("Choose your preferred language:", ["English", "Spanish", "Hindi"])
text = translations[language]

# Session state init
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'patient' not in st.session_state:
    st.session_state.patient = None

# Step 0: Chat greeting
prompt = st.text_input(text["greet"])
if prompt.lower() in ["hello", "hi", "hola", "नमस्ते"] and st.session_state.step == 0:
    st.session_state.step = 1

# Step 1: Get Patient ID and Name
if st.session_state.step == 1:
    st.subheader(text["patient_prompt"])
    patient_id = st.text_input(text["enter_id"])
    full_name = st.text_input(text["enter_name"])
    if patient_id and full_name:
        match = match_patient(patient_id, full_name)
        if match is not None:
            st.session_state.patient = match
            st.success(text["checked_in"].format(full_name))
            st.session_state.step = 2
        else:
            st.error(text["not_found"])

# Step 2: Booking symptoms
if st.session_state.step == 2 and "book" in prompt.lower():
    st.write(text["symptom_greet"].format(st.session_state.patient['First_Name'] + " " + st.session_state.patient['Last_Name']))
    symptoms = st.multiselect(text["choose_symptoms"], ["Headache", "Fever", "Cough", "Stomach pain"])
    if symptoms:
        specialty = "General Physician"
        st.write(text["recommend"].format(specialty))
        if st.button(text["proceed_btn"]):
            st.session_state.step = 3
            st.session_state.specialty = specialty

# Step 3: Choose doctor and time
if st.session_state.step == 3:
    matched_docs = doctors[doctors["Specialty"] == st.session_state.specialty]
    if not matched_docs.empty:
        selected_doctor = st.selectbox(text["choose_doctor"], matched_docs["Doctor_Name"])
        selected_time = st.selectbox(text["choose_time"], ["9 AM - 10 AM", "10 AM - 11 AM", "11 AM - 12 PM"])
        if st.button(text["confirm_btn"]):
            st.session_state.step = 4
            patient = st.session_state.patient
            patient_name = patient['First_Name'] + " " + patient['Last_Name']
            emergency_name = patient['Emergency_Contact_Name']
            appointment_date = "2025-05-06"

            st.markdown(f"""
            {text['confirmation']}  
            {text['patient']} {patient_name}  
            {text['doctor']} {selected_doctor}  
            {text['datetime']} {appointment_date} at {selected_time}  
            {text['location']}  
            {text['insurance']} {patient['Insurance_Type']}  

            {text['reminder'].format(emergency_name)}  

            {text['bye'].format(patient_name)}
            """)

            st.session_state.appointment_confirmed = True

# Step 4: Simulate Email Reminder
if st.session_state.get('appointment_confirmed'):
    st.write(text["ask_reminder"])
    choice = st.radio(text["radio_reminder"], ["Yes", "No"], key="simulate_email")
    if choice == "Yes":
        if st.button("Simulate Email Reminder"):
            st.success(text["reminder_success"])
            st.info(text["reminder_bye"])
    else:
        st.info(text["reminder_skip"])

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.radio("Go to", ["Chatbot", "Doctor Availability", "Patient Data"])
