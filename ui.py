import streamlit as st
import requests

# Streamlit UI Title
st.title("🤖 Emotional AI Chatbot")

# Sidebar for Adjusting Emotional Parameters
st.sidebar.header("Adjust Emotional Parameters")

parameters = {
    "valence": st.sidebar.slider('Valence', 1, 7, 4),
    "arousal": st.sidebar.slider('Arousal', 1, 7, 4),
    "selectionThreshold": st.sidebar.slider('Selection Threshold', 1, 7, 4),
    "resolution": st.sidebar.slider('Resolution', 1, 7, 4),
    "goalDirectedness": st.sidebar.slider('Goal Directedness', 1, 7, 4),
    "securingRate": st.sidebar.slider('Securing Rate', 1, 7, 4)
}

# Display Selected Parameters
st.sidebar.write("### Current Emotional State:")
for param, value in parameters.items():
    st.sidebar.write(f"- {param}: {value}")

# Function to Update Emotional State
def update_emotions(params):
    try:
        response = requests.post("http://127.0.0.1:5000/calculate-emotions", json=params)
        response.raise_for_status()
        data = response.json()
        st.sidebar.write(f"🔹 Anger: {round(data['anger'], 2)}")
        st.sidebar.write(f"🔹 Sadness: {round(data['sadness'], 2)}")
    except requests.RequestException as e:
        st.sidebar.error(f"❌ Error updating emotions: {e}")

# Update Emotions Button
if st.sidebar.button("Update Emotional State"):
    update_emotions(parameters)

# Chat Interface
st.write("### Chat with the AI")
user_input = st.text_input("Type your message...", key="user_input")
send_button = st.button("Send")

# Session state for message history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Send Message & Display Chatbot Response
if send_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        # Send message to Flask API
        response = requests.post("http://127.0.0.1:5000/send-message", json={"message": user_input, "parameters": parameters})
        response.raise_for_status()
        bot_response = response.json().get("reply", "No response from server")
        
        # Append bot message to chat history
        st.session_state.messages.append({"role": "bot", "content": bot_response})
    except requests.RequestException as e:
        st.session_state.messages.append({"role": "bot", "content": f"Error: {e}"})

    # Clear input field
    st.text_input("Type your message...", value="", key="user_input_clear")

# Display Chat History
for msg in st.session_state.messages:
    if msg['role'] == "user":
        st.write(f"**You:** {msg['content']}")
    else:
        st.write(f"**Bot:** {msg['content']}")
