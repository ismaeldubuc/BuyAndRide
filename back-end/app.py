import mysql.connector
from flask import Flask, request, jsonify, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from fonction import register, login, profile, logout, create_vehicle, update_vehicle, delete_vehicle, get_vehicle
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.secret_key = 'buyandride'


bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD') 
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'], 
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

cursor = mysql.cursor(dictionary=True)

@app.route("/")
def home():
    return "Hello, World!"

@app.route('/register', methods=['POST'])
def register_route():
    return register()

@app.route('/login', methods=['POST'])
def login_route():
    return login()

@app.route('/profile', methods=['GET', 'POST'])
def profile_route():
    return profile()

@app.route('/logout', methods=['POST'])
def logout_route():
    return logout()

@app.route("/api/create-vehicle", methods=["POST"])
def create_vehicle_func():
    return create_vehicle()

@app.route('/static/uploads/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/uploads', filename)

@app.route("/api/update-vehicle", methods=["PUT"])
def update_vehicle_func():
    return update_vehicle()

@app.route("/api/delete-vehicle", methods=["DELETE"])
def delete_vehicle_func():
    return delete_vehicle()

@app.route("/api/get-vehicle", methods=["GET"])
def get_vehicle_func():
    return get_vehicle()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)