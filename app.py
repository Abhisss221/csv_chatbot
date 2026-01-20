# app.py
from flask import Flask, render_template, request, jsonify
from bot3 import initialize_db, ask_bot

app = Flask(__name__)

# Initialize DB once
con = initialize_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please ask a valid question."})

    answer = ask_bot(con, question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

