
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>TechCorp AI Assistant</title>
    </head>
    <body>
        <h1>TechCorp AI Assistant</h1>

        <textarea id="message" placeholder="Ask me anything..."
        style="width:700px;height:150px;font-size:18px;"></textarea>
        <button onclick="sendMessage()">Send</button>

        <h3>AI Response:</h3>
        <pre id="response"></pre>

        <script>
        async function sendMessage() {
            const message = document.getElementById("message").value;

            const result = await fetch("/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({message: message})
            });

            const data = await result.json();

            document.getElementById("response").textContent =
                data.response;
        }
        </script>
    </body>
    </html>
    """

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "user", "content": user_message}
            ],
            "stream": False
        }
    )

    ai_response = response.json()["message"]["content"]

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

