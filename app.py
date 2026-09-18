from flask import Flask, request, jsonify, render_template
import subprocess
import sys
import os

app = Flask(__name__)

process = None  # keeps track of the running assistant process

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global process

    if process and process.poll() is None:
        process.terminate()

    data = request.json
    lang = data.get("lang", "en")

    process = subprocess.Popen(
        [sys.executable, "assistant.py", lang],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

    return jsonify({"status": "started", "lang": lang})

@app.route("/stop", methods=["POST"])
def stop():
    global process
    if process and process.poll() is None:
        process.terminate()
        return jsonify({"status": "stopped"})

    return jsonify({"status": "not running"})

if __name__ == "__main__":
    print("\n✅ Open your browser and go to: http://localhost:5000\n")
    app.run(debug=True, port=5000)