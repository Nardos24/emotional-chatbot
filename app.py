from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
CORS(app)

# 🔹 Set up OpenRouter as the chatbot LLM
llm = ChatOpenAI(
    temperature=0.7,
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

# 🔹 Use LangChain Memory to retain chat context
memory = ConversationBufferMemory()
conversation_chain = ConversationChain(llm=llm, memory=memory)

# 🔹 Serve Frontend
@app.route('/')
def index():
    return render_template("index.html")

# 🔹 Emotional State Calculation
@app.route('/calculate-emotions', methods=['POST'])
def calculate_emotions():
    data = request.json
    try:
        # Convert values to float to ensure numeric operations
        valence = float(data.get("valence", 4))  # 1-7 scale
        arousal = float(data.get("arousal", 4))  # 1-7 scale
        selection_threshold = float(data.get("selectionThreshold", 4))  # 1-7 scale
        resolution = float(data.get("resolution", 4))  # 1-7 scale
        goal_directedness = float(data.get("goalDirectedness", 4))  # 1-7 scale
        securing_rate = float(data.get("securingRate", 4))  # 1-7 scale

        # Calculate emotions using the correct scale (1-5)
        anger = min(7, max(1, 1 + ((1 - valence / 7) * (arousal / 7) * (goal_directedness / 7) * (selection_threshold / 7) * 6)))
        sadness = min(7, max(1, 1 + ((1 - valence / 7) * (1 - arousal / 7) * (securing_rate / 7) * 6)))

        print(f"🔹 Calculated Emotions → Anger: {round(anger, 2)}, Sadness: {round(sadness, 2)}")

        return jsonify({"anger": round(anger, 2), "sadness": round(sadness, 2)})
    
    except ValueError as e:
        print(f"❌ Error converting values: {e}")
        return jsonify({"error": "Invalid input data"}), 400

# 🔹 Chatbot Response with Emotional Awareness
@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    try:
        message = data.get("message", "")
        parameters = data.get("parameters", {})

        valence = float(parameters.get("valence", 4))
        arousal = float(parameters.get("arousal", 4))
        selection_threshold = float(parameters.get("selectionThreshold", 4))
        resolution = float(parameters.get("resolution", 4))
        goal_directedness = float(parameters.get("goalDirectedness", 4))
        securing_rate = float(parameters.get("securingRate", 4))

        anger = min(7, max(1, 1 + ((1 - valence / 7) * (arousal / 7) * (goal_directedness / 7) * (selection_threshold / 7) * 6)))
        sadness = min(7, max(1, 1 + ((1 - valence / 7) * (1 - arousal / 7) * (securing_rate / 7) * 6)))

        # 🟢 Enhanced Emotional Context for Chatbot
        emotional_context = f"""
I am currently experiencing the following emotions:
- 😡 Anger Level: {round(anger, 2)}
- 😢 Sadness Level: {round(sadness, 2)}

Please take my emotions into account when responding.
""".strip()

        user_input = f"{emotional_context}\nUser: {message}"

        print("\n🔹 Sending to OpenRouter:")
        print(user_input)

        response = conversation_chain.run(user_input)
        return jsonify({"reply": response})
    
    except ValueError as e:
        print(f"❌ Error processing message: {e}")
        return jsonify({"error": "Invalid input data"}), 400

if __name__ == "__main__":
    print("🔹 Flask Server is Starting...")
    app.run(debug=True, host="0.0.0.0", port=5000)
