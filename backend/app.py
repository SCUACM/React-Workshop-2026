import firebase_admin
from firebase_admin import credentials, firestore

from flask import Flask, jsonify, request, send_from_directory
app = Flask(__name__, static_folder="../ReactWorkshop/dist", static_url_path="/")

from flask_cors import CORS
CORS(app, origins=["http://localhost:5173"])

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/firebase/get" , methods=["GET"])
def firebase_get():
    db = firestore.client()
    doc = db.collection("clicker").document("counter").get()
    if doc.exists:
        return jsonify(doc.to_dict())
    return jsonify({"error": "Document not found"}), 404

@app.route("/firebase/set", methods=["POST"])
def firebase_set():
    data = request.get_json()
    print("Received data for Firebase update:", data)
    db.collection("clicker").document("counter").set(data)
    return jsonify({"message": "Data updated successfully"}), 200

if __name__ == "__main__":
    app.run(port=8080,debug=True)