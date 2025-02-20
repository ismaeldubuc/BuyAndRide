import psycopg2
import psycopg2.extras
from flask import Flask, request, jsonify, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from fonction import register, login, profile, logout, create_vehicle, update_vehicle, delete_vehicle, get_vehicle , save_devis,list_vehicules,get_vehicule,add_vehicule,get_vehicle_by_id,update_etat_vehicule,get_achat_vehicule, get_louer_vehicule,filter_vehicules,get_marques,get_modeles, modif_profil
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app, resources={r"/api/*": {
    "origins": "https://main.d3bzhfj3yrtaed.amplifyapp.com",
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
    "supports_credentials": True
}})


app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Configuration de la connexion à PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('PG_HOST', 'hetic.cd5ufp6fsve3.us-east-1.rds.amazonaws.com'),
        port=os.getenv('PG_PORT', '5432'),
        database=os.getenv('PG_DB', 'groupe4'),
        user=os.getenv('PG_USER', 'postgres'),
        password=os.getenv('PG_PASSWORD', 'LeContinent!')
    )
    return conn

@app.route("/")
def home():
    return "Hello, World!"

# Routes
@app.route('/register', methods=['POST'])
def register_route():
    return register()

@app.route('/login', methods=['POST'])
def login_route():
    return login()

@app.route('/profile', methods=['GET'])
def profile_route():
    return profile()

@app.route('/modif_profil', methods=['POST'])
def modif_profil_route():
    return modif_profil()

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
