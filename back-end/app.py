import psycopg2
import psycopg2.extras
from flask import Flask, request, jsonify, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from fonction import register, login, profile, logout, create_vehicle, update_vehicle, delete_vehicle, get_vehicle , save_devis,get_vehicule,get_vehicle_by_id,update_type_vehicule,get_achat_vehicule, get_louer_vehicule,filter_vehicules,get_marques,get_modeles, modif_profil
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Configuration de la connexion à PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('PG_HOST'),
            port=os.getenv('PG_PORT'),
            database=os.getenv('PG_DB'),
            user=os.getenv('PG_USER'),
            password=os.getenv('PG_PASSWORD')
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise

@app.route("/")
def home():
    return "Hello, World!"

# Routes
@app.route('/api/register', methods=['POST'])  #Inscription
def register_route():
    return register()

@app.route('/api/login', methods=['POST'])  #Connexion
def login_route():
    return login()

@app.route('/api/profile', methods=['GET'])  #Affichage du profil
def profile_route():
    return profile()

@app.route('/api/modif_profil', methods=['POST'])  #Modification du profil
def modif_profil_route():
    return modif_profil()

@app.route('/api/logout', methods=['POST'])  #Déconnexion
def logout_route():
    return logout()

@app.route("/api/create-vehicule", methods=["POST"])  #Création d'un véhicule
def create_vehicle_func():
    return create_vehicle()

@app.route('/api/vehicules/<int:id>', methods=['GET'])  #Affichage d'un véhicule
def get_vehicule_route(id):
    return get_vehicule(id)

@app.route("/api/update-vehicule/<int:id>", methods=["PUT"])  #Modification d'un véhicule
def update_vehicle_func(id):
    return update_vehicle(id)

@app.route("/api/delete-vehicule/<int:id>", methods=["DELETE"])  #Suppression d'un véhicule
def delete_vehicle_func(id):
    return delete_vehicle(id)

@app.route("/api/get-vehicule", methods=["GET"])  #Affichage de tous les véhicules
def get_vehicle_func():
    return get_vehicle()

@app.route("/api/get-vehicule/<int:id>", methods=["GET"])  #Affichage d'un véhicule spécifique
def get_vehicle_by_id_func(id):
    return get_vehicle_by_id(id)

@app.route('/api/devis/<int:vehicule_id>', methods=['POST'])  #Enregistrement d'un devis
def save_devis_route(vehicule_id):
    if not request.data:
        return jsonify({"error": "Aucune donnée PDF fournie"}), 400
    return save_devis(vehicule_id, request.data)

@app.route('/api/update-type-vehicule/<int:id>', methods=['PUT'])  #Modification du type de véhicule achat/location
def update_etat_type_route(id):
    return update_type_vehicule(id)

@app.route('/api/get-achat-vehicule', methods=['GET'])  #Affichage des véhicules d'achat
def get_achat_vehicule_route():
    return get_achat_vehicule()

@app.route('/api/get-louer-vehicule', methods=['GET'])  #Affichage des véhicules de location
def get_louer_vehicule_route():
    return get_louer_vehicule()

@app.route('/api/vehicules/filter', methods=['POST'])  #Filtre des véhicules
def filter_vehicules_route():
    return filter_vehicules()

@app.route('/api/marques', methods=['GET'])  #Affichage des marques
def get_marques_route():
    return get_marques()

@app.route('/api/modeles/<marque>', methods=['GET'])  #Affichage des modèles
def get_modeles_route(marque):
    return get_modeles(marque)

@app.route('/static/uploads/<path:filename>') #?
def serve_image(filename):
    return send_from_directory('static/uploads', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
