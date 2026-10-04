from flask import Flask, request, jsonify, send_from_directory
import joblib
import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

model = joblib.load(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "model.pkl")
)

app = Flask(__name__)

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


@app.route("/register-page")
def register_page():
    return send_from_directory("../frontend", "register.html")

@app.route("/login-page")
def login_page():
    return send_from_directory(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend"),
        "login.html"
    )

@app.route("/predict-page")
def predict_page():
    return send_from_directory(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend"),
        "predict.html"
    )

@app.route("/login.js")
def login_js():
    return send_from_directory(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend"),
        "login.js"
    )

@app.route("/predict.js")
def predict_js():
    return send_from_directory(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend"),
        "predict.js"
    )

@app.route("/register.js")
def register_js():
    return send_from_directory(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend"),
        "register.js"
    )


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

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    features = [
        data["HighBP"],
        data["HighChol"],
        data["CholCheck"],
        data["BMI"],
        data["Smoker"],
        data["Stroke"],
        data["HeartDiseaseorAttack"],
        data["PhysActivity"],
        data["Fruits"],
        data["Veggies"],
        data["HvyAlcoholConsump"],
        data["AnyHealthcare"],
        data["NoDocbcCost"],
        data["GenHlth"],
        data["MentHlth"],
        data["PhysHlth"],
        data["DiffWalk"],
        data["Sex"],
        data["Age"],
        data["Education"],
        data["Income"]
    ]

    prediction = model.predict([features])[0]

    return jsonify({
        "prediction": int(prediction)
    })

if __name__ == "__main__":
    app.run(debug=True)