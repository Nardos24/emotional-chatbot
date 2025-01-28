import streamlit as st
import requests
import json

# Title
st.title("🤖 Emotional AI Chatbot")

# Sidebar for Emotional Parameters
st.sidebar.header("Adjust Emotional Parameters")

# Sliders for parameters
parameters = {
    "valence": st.sidebar.slider('Valence', 1, 7, 4),
    "arousal": st.sidebar.slider('Arousal', 1, 7, 4),
    "selectionThreshold": st.sidebar.slider('Selection Threshold', 1, 7, 4),
    "resolution": st.sidebar.slider('Resolution', 1, 7, 4),
    "goalDirectedness": st.sidebar.slider('Goal Directedness', 1, 7, 4),
    "securingRate": st.sidebar.slider('Securing Rate', 1, 7, 4)
}

# Display the current values of the sliders
st.sidebar.write("Current Parameter Values:")
for param, value in parameters.items():
    st.sidebar.write(f"- {param.capitalize()}: {value}")

# Function to update and display emotions
def update_emotions(params):
    try:
        response = requests.post("http://127.0.0.1:5000/calculate-emotions", json=params)
        response.raise_for_status()
        data = response.json()
        st.sidebar.write(f"🔹 Anger: {round(data['anger'])}")
        st.sidebar.write(f"🔹 Sadness: {round(data['sadness'])}")
    except requests.RequestException as e:
        st.sidebar.error(f"❌ Error updating emotions: {e}")

# Use a button to update emotions
if st.sidebar.button("Update Emotional State"):
    update_emotions(parameters)

# Chat interface
user_input = st.text_input("Type your message...", key="user_input")
send_button = st.button("Send")

# Session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

if send_button and user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        # Send message to backend
        response = requests.post("http://127.0.0.1:5000/send-message", json={"message": user_input, "parameters": parameters})
        response.raise_for_status()
        bot_response = response.json().get("reply", "No response from server")
        # Append bot message
        st.session_state.messages.append({"role": "bot", "content": bot_response})
    except requests.RequestException as e:
        st.session_state.messages.append({"role": "bot", "content": f"Error: {e}"})
    
    # Clear the input after sending
    # Change the key here for uniqueness
    st.text_input("Type your message...", value="", key="user_input_clear")

# Display messages
for msg in st.session_state.messages:
    if msg['role'] == "user":
        st.write(f"<b>You:</b> {msg['content']}", unsafe_allow_html=True)
    else:
        st.write(f"<b>Bot:</b> {msg['content']}", unsafe_allow_html=True)