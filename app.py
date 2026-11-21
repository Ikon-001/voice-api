from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def status():
    return jsonify({"status": "ok"})
