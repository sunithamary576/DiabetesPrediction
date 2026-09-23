from flask import Flask
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

print("MySQL connected successfully!")

cursor = db.cursor()
cursor.execute("SHOW TABLES")

print("Tables in database:")
for table in cursor:
    print(table)


@app.route("/")
def home():
    return "Diabetes Risk Prediction API is running!"


if __name__ == "__main__":
    app.run(debug=True)