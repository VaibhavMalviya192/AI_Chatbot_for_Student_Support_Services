import streamlit as ui
import google.generativeai as genai

# 1. Page Configuration & Title Layout
ui.set_page_config(page_title="Student Support AI", page_icon="🎓", layout="centered")
ui.title("🎓 Student Support Service Chatbot")
ui.markdown(
    "Welcome to the automated Student Support Desk! This AI assistant helps with queries regarding "
    "**admissions, sessional exam schedules, campus navigation, and library resources.**"
)
ui.hr()

# 2. Secure API Key Management via Sidebar
with ui.sidebar:
    ui.header("🔑 Authentication")
    ui.markdown("To run the assistant, please input your Gemini API Key below.")
    api_key_input = ui.text_input("Google Gemini API Key", type="password", placeholder="AIzaSy...")
    ui.info("Get a free API key from Google AI Studio.")

# Stop execution safely if the user hasn't provided an API key yet
if not api_key_input:
    ui.warning("⚠️ Action Required: Please enter your Google Gemini API Key in the left sidebar to activate the chatbot.")
    ui.stop()

# Configure the API with the entered key
genai.configure(api_key=api_key_input)

# 3. Define the Chatbot's Academic Persona
SYSTEM_INSTRUCTION = """
You are an expert AI Assistant for a University's Student Support Service. 
Your goal is to help students with academic queries, sessional exam preparations, campus navigation, 
library hours, and general admission guidance. Always maintain a warm, helpful, and peer-like tone. 
Keep answers concise and well-structured using bullet points where appropriate. 
If a student asks a highly specific legal or administrative policy question you do not know, 
politely direct them to the university registrar's office.
"""

# Initialize Gemini Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

# 4. Initialize Persistent Chat History in Streamlit Memory
if "chat" not in ui.session_state:
    ui.session_state.chat = model.start_chat(history=[])

# 5. UI Showcase: Suggested Quick-Start Questions
ui.markdown("##### 💡 Frequently Asked Questions")
col1, col2 = ui.columns(2)

# Helper function to inject preset questions into the system
def preset_click(question_text):
    ui.session_state.pending_preset = question_text

# Create interactive quick-click buttons for evaluation
with col1:
    if ui.button("📅 When are sessional exams held?", use_container_width=True):
        preset_click("When are sessional exams typically held during the semester, and what is the best way to prepare?")
with col2:
    if ui.button("📚 How do I access library resources?", use_container_width=True):
        preset_click("How do I access digital library resources and check book availability?")

# Check if a preset button was clicked
user_prompt = ui.session_state.pop("pending_preset", None)

# 6. Display Ongoing Conversation History
# Maps Gemini's role ('model') to Streamlit's preferred UI role ('assistant')
for message in ui.session_state.chat.history:
    ui_role = "user" if message.role == "user" else "assistant"
    with ui.chat_message(ui_role):
        ui.markdown(message.parts[0].text)

# 7. Handle Active User Input (Chat Box)
chat_box_input = ui.chat_input("Ask a question about your course or campus...")
if chat_box_input:
    user_prompt = chat_box_input

# 8. Process and Render Responses
if user_prompt:
    # Display the user's message immediately
    with ui.chat_message("user"):
        ui.markdown(user_prompt)
    
    # Generate and stream the AI assistant response
    with ui.chat_message("assistant"):
        response_placeholder = ui.empty()
        with ui.spinner("Typing..."):
            # Sends message through the active, state-saved chat session
            response = ui.session_state.chat.send_message(user_prompt)
            response_placeholder.markdown(response.text)
