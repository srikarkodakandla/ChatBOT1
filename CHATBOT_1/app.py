from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Ollama server is running in the same container, so we use localhost
OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL = "phi3:mini" # A small, fast model perfect for a free web service

@app.route('/')
def index():
    """Serves the main chat page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handles chat requests."""
    data = request.json
    user_message = data.get("message")
    conversation_history = data.get("history")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Add the new user message to the history
    conversation_history.append({"role": "user", "content": user_message})

    # Prepare payload for Ollama
    payload = {
        "model": MODEL,
        "messages": conversation_history,
        "stream": False
    }

    try:
        # Send request to Ollama
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        
        response_data = response.json()
        assistant_message = response_data["message"]["content"]
        
        # Add assistant's response to history
        conversation_history.append({"role": "assistant", "content": assistant_message})

        return jsonify({"response": assistant_message, "history": conversation_history})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Could not connect to Ollama: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)