import os

import requests
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__, static_folder="../ReactWorkshop/dist", static_url_path="/")

# CORS only matters for browsers (our React app). Postman and the terminal ignore it.
CORS(app, origins=["http://localhost:5173"])

# ---------------------------------------------------------------------------
# Firebase (from the Firebase workshop)
# Firebase is OPTIONAL for this workshop. If credentials.json is missing,
# the server still starts and only the /firebase routes are turned off.
# ---------------------------------------------------------------------------
CREDENTIALS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json")

db = None
if os.path.exists(CREDENTIALS_PATH):
    cred = credentials.Certificate(CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase connected!")
else:
    print("No credentials.json found. Firebase routes are disabled, everything else works.")


def firebase_disabled():
    return jsonify(error="Firebase is not set up. Add credentials.json to the backend folder."), 503


@app.route("/firebase/get", methods=["GET"])
def firebase_get():
    if db is None:
        return firebase_disabled()
    doc = db.collection("clicker").document("counter").get()
    if doc.exists:
        return jsonify(doc.to_dict())
    return jsonify({"error": "Document not found"}), 404


@app.route("/firebase/set", methods=["POST"])
def firebase_set():
    if db is None:
        return firebase_disabled()
    data = request.get_json()
    print("Received data for Firebase update:", data)
    db.collection("clicker").document("counter").set(data)
    return jsonify({"message": "Data updated successfully"}), 200


# ---------------------------------------------------------------------------
# API Workshop: making our own API
# ---------------------------------------------------------------------------

@app.route("/hello")
def hello():
    """
    returns
    {
        "message": "Hello, World!"
    }
    """
    return jsonify(message="Hello, World!")


@app.route("/add")
def add():
    """
    Passing data way #1: URL query parameters
    access via http://127.0.0.1:8080/add?a=2&b=3
    returns
    {
        "result": 5
    }
    """
    a = request.args.get("a")
    b = request.args.get("b")
    if a is None or b is None:
        return jsonify(error="Missing 'a' and/or 'b' URL parameters"), 400
    try:
        return jsonify(result=int(a) + int(b))
    except ValueError:
        return jsonify(error="'a' and 'b' must be whole numbers"), 400


@app.route("/acm-token")
def acm_token():
    """
    Getting the ACM token like we did in Postman, but in Python
    returns
    {
        "data": { ... },
        "token": "..."
    }
    """
    URL = "https://api.scuacm.com/v1/token"
    key = "acmKey123"  # In a real app, keep keys in a .env file, never in your code!
    data = requests.get(URL, params={"key": key}).json()  # expands to .../v1/token?key=acmKey123
    return jsonify(data=data, token=data.get("token"))


@app.route("/acm-data", methods=["POST"])
def acm_data():
    """
    Passing data way #2: a JSON body
    needs JSON body as
    {
        "token": "..."
    }
    returns
    {
        "data": "..."
    }
    """
    URL = "https://api.scuacm.com/v1/data"
    body = request.get_json(silent=True)
    if not body:
        return jsonify(error="Missing JSON body"), 400
    token = body.get("token")
    if not token:
        return jsonify(error="Missing 'token' in body"), 400
    headers = {"Authorization": f"Bearer {token}"}  # the token goes in the header with the "Bearer" auth method
    response = requests.get(URL, headers=headers)
    data = response.json()
    if response.status_code != 200:
        return jsonify(error=data.get("error", "Request failed")), response.status_code
    return jsonify(data=data.get("message"))


if __name__ == "__main__":
    app.run(port=8080, debug=True)
