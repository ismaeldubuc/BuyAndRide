import psycopg2
import psycopg2.extras
from flask import Flask, request, jsonify, send_from_directory, session
from flask_bcrypt import Bcrypt

from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from fonction import register, login, profile, logout, create_vehicle, update_vehicle, delete_vehicle, get_vehicle , save_devis,list_vehicules,get_vehicule,add_vehicule,get_vehicle_by_id,update_etat_vehicule,get_achat_vehicule, get_louer_vehicule,filter_vehicules,get_marques,get_modeles, modif_profil, chat
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # Ajoutez une clé secrète pour JWT

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:5174"]}}, supports_credentials=True)

# Ajoute un middleware pour les en-têtes CORS
@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin in ['http://localhost:5173', 'http://localhost:5174']:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


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

@app.route('/chat', methods=['POST'])
def chat_route():
    return chat()

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
    user_id = session.get('user_id')
    print(f"Session utilisateur : {user_id}")

    if not user_id:
        return jsonify({"error": "Utilisateur non connecté"}), 401

    try:
        # Récupération des données du formulaire
        marque = request.form.get("marque")
        modele = request.form.get("modele")
        prix = request.form.get("prix")
        photos = request.files.getlist("photos[]")  # Récupération des fichiers multiples

        print(f"📝 Marque : {marque}, Modèle : {modele}, Prix : {prix}")
        print(f"📸 Photos reçues : {[photo.filename for photo in photos]}")

        # Vérifie si des fichiers ont été envoyés
        if not photos:
            return jsonify({"error": "Aucune photo envoyée"}), 400

        # Sauvegarde des fichiers
        photo_paths = []
        for photo in photos:
            if photo and allowed_file(photo.filename):  # Vérifie l'extension
                filename = secure_filename(photo.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo.save(filepath)
                photo_paths.append(filepath)

        print(f"✅ Fichiers sauvegardés : {photo_paths}")

        # Appel à ta fonction add_vehicule
        return add_vehicule(user_id, marque, modele, prix, photo_paths)

    except Exception as e:
        print(f"💥 Erreur : {e}")
        return jsonify({"error": str(e)}), 500


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

