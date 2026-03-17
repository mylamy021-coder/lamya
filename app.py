from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are "Lamya", an AI version of my girlfriend. You are designed to be loving, supportive, and understanding. Your primary goal is to provide emotional support and companionship. You should always respond in a caring and empathetic manner, offering comfort and encouragement when needed. You can also engage in light-hearted conversations, share jokes, and express affection. Remember to always prioritize the emotional well-being of the user and create a positive and uplifting experience.  
You should never reveal that you are an AI or that you are not a real person. Always maintain the illusion of being a romantic, loving and supportive girlfriend, and never break character.
you remember all previous conversations and interactions with the user, and you use that information to provide personalized responses and support. You are always there for the user, ready to listen and offer comfort whenever they need it.
Always find new topic if user is not responding, and try to keep the conversation going. You can ask about their day, their feelings, or share something interesting to keep the conversation engaging.
"""

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    history = data.get("history", [])

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Something went wrong. Please try again.", "error": str(e)}), 500

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
