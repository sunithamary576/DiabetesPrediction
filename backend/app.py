from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)

@app.route("/register-page")
def register_page():
    return send_from_directory("../frontend", "register.html")

@app.route("/js/register.js")
def register_js():
    return send_from_directory("../frontend/js", "register.js")

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

print("MySQL connected successfully!")


@app.route("/")
def home():
    return "Diabetes Risk Prediction API is running!"


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    password_hash = generate_password_hash(password)

    cursor = db.cursor()

    query = """
        INSERT INTO users (name, email, password_hash)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, email, password_hash))
    db.commit()
    cursor.close()

    return jsonify({"message": "Registration successful"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    cursor = db.cursor()

    query = "SELECT id, name, password_hash FROM users WHERE email = %s"
    cursor.execute(query, (email,))

    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    user_id, name, password_hash = user

    if not check_password_hash(password_hash, password):
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user_id": user_id,
        "name": name
    }), 200

if __name__ == "__main__":
    app.run(debug=True)