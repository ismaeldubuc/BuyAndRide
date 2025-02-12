

from flask import Flask, request, jsonify, send_from_directory, url_for, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import mysql.connector
import os
from werkzeug.utils import secure_filename
from fonction import add_vehicule, get_vehicule, list_vehicules, register, login, profile, logout, create_vehicle, update_vehicle, delete_vehicle, get_vehicle
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)


app.secret_key = 'buyandride'
bcrypt = Bcrypt(app)

CORS(app, supports_credentials=True)

# Database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pythonlogin"
)


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

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

# Upload configuration
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize database
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS pythonlogin")
cursor.execute("USE pythonlogin")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nom VARCHAR(100),
        prenom VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicules (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        marque VARCHAR(100),
        modele VARCHAR(100),
        prix DECIMAL(10,2),
        kilometrage INT,
        energie VARCHAR(50),
        type VARCHAR(50),
        description TEXT,
        photo1 VARCHAR(255),
        photo2 VARCHAR(255),
        photo3 VARCHAR(255),
        photo4 VARCHAR(255),
        photo5 VARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")
db.commit()

def save_file(file_key):
    file = request.files.get(file_key)
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        absolute_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(absolute_path)
        return os.path.join('uploads', filename)
    return None

# Authentication routes
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

@app.route('/vehicules', methods=['GET'])
def list_vehicules_route():
      return list_vehicules()

@app.route('/vehicules/<int:id>', methods=['GET'])
def get_vehicule_route(id):
  return get_vehicule(id)

@app.route('/static/uploads/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/uploads', filename)

@app.route('/vehicules', methods=['POST'])
def add_vehicule_route():
   return add_vehicule()

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/api/create-vehicle", methods=["POST"])
def create_vehicle_func():
    return create_vehicle()

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