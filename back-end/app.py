import mysql.connector
from flask import Flask, request, jsonify, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from fonction import register, login, profile, logout, create_vehicle, update_vehicle, delete_vehicle, get_vehicle , save_devis,list_vehicules,get_vehicule,add_vehicule,get_vehicle_by_id,update_etat_vehicule,get_achat_vehicule, get_louer_vehicule,filter_vehicules,get_marques,get_modeles
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

@app.route('/vehicules', methods=['GET'])
def list_vehicules_route():
      return list_vehicules()

@app.route('/vehicules/<int:id>', methods=['GET'])
def get_vehicule_route(id):
  return get_vehicule(id)

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

@app.route("/api/get-vehicle/<int:id>", methods=["GET"])
def get_vehicle_by_id_func(id):
    return get_vehicle_by_id(id)

@app.route('/vehicules', methods=['POST'])
def add_vehicule_route():
   return add_vehicule()

@app.route('/api/devis/<int:vehicule_id>', methods=['POST'])
def save_devis_route(vehicule_id):
    if not request.data:
        return jsonify({"error": "Aucune donnée PDF fournie"}), 400
    return save_devis(vehicule_id, request.data)
@app.route("/api/filter-vehicles", methods=["GET"])
def filter_vehicles_func():
    return filter_vehicles()

@app.route('/api/update-etat-vehicule', methods=['PUT'])
def update_etat_vehicule_route():
    return update_etat_vehicule()

@app.route('/api/get-achat-vehicule', methods=['GET'])
def get_achat_vehicule_route():
    return get_achat_vehicule()

@app.route('/api/get-louer-vehicule', methods=['GET'])
def get_louer_vehicule_route():
    return get_louer_vehicule()

@app.route('/vehicules/filter', methods=['POST'])
def filter_vehicules_route():
    return filter_vehicules()

@app.route('/marques', methods=['GET'])
def get_marques_route():
    return get_marques()

@app.route('/modeles/<marque>', methods=['GET'])
def get_modeles_route(marque):
    return get_modeles(marque)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)