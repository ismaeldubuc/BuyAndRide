import psycopg2
import psycopg2.extras
from flask import Flask, request, jsonify, send_from_directory, Blueprint, session as flask_session
from flask_bcrypt import Bcrypt

from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import fonction
from dotenv import load_dotenv
import os
import logging
import boto3
from botocore.exceptions import ClientError
from flask_session import Session
from redis import Redis
from flask_talisman import Talisman
from logging.handlers import RotatingFileHandler
from flask_compress import Compress
from datetime import datetime, timedelta
from database import get_db_connection
from psycopg2.extras import DictCursor
from fonction import upload_pdf_to_s3  # Ajoutez cet import
from flask_restful import Api

# Set up logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'votre_clé_secrète_par_défaut')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'votre_clé_jwt_par_défaut')

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

api = Blueprint('api', __name__, url_prefix='/api')

# Configuration CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

# Configuration de la session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 heure en secondes

# Configuration de la base de données
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/buyandride')

# Configuration AWS
app.config['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
app.config['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')
app.config['AWS_REGION'] = os.getenv('AWS_REGION', 'eu-west-3')
app.config['S3_BUCKET'] = os.getenv('S3_BUCKET', 'buyandride')

Session(app)

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Désactivez Talisman en développement ou modifiez sa configuration
if os.getenv('FLASK_ENV') != 'production':
    app.config['TALISMAN_ENABLED'] = False
else:
    Talisman(app, 
        content_security_policy={
            'default-src': "'self'",
            'img-src': ['*', 'data:', 'https:'],
            'script-src': ["'self'", "'unsafe-inline'"],
            'style-src': ["'self'", "'unsafe-inline'"]
        }
    )

Compress(app)

# Routes API
@api.route('/login', methods=['POST'])
def login_route():
    return fonction.login()

@api.route('/check-login', methods=['GET'])
def check_login_route():
    try:
        return fonction.check_login()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/register', methods=['POST'])
def register_route():
    return fonction.register()

@api.route('/profile', methods=['GET'])
def profile_route():
    return fonction.profile()

@api.route("/create-vehicle", methods=["POST"])
def create_vehicle_func():
    return fonction.create_vehicle()

@api.route('/chat', methods=['POST', 'OPTIONS'])
def chat_route():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 200
    return fonction.chat()

@api.route('/modif_profil', methods=['POST'])
def modif_profil_route():
    return fonction.modif_profil()

@api.route('/logout', methods=['POST'])
def logout_route():
    return fonction.logout()

@api.route('/vehicules', methods=['GET'])
def get_vehicules_route():
    return fonction.get_vehicules()

@api.route('/vehicules/<int:id>', methods=['GET'])
def get_vehicule_route(id):
    return fonction.get_vehicule_by_id(id)

@api.route('/static/uploads/<path:filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@api.route("/update-vehicle", methods=["PUT"])
def update_vehicle_func():
    return fonction.update_vehicle()

@api.route("/delete-vehicle", methods=["DELETE"])
def delete_vehicle_func():
    return fonction.delete_vehicle()

@api.route("/get-vehicle", methods=["GET"])
def get_vehicle_func():
    return fonction.get_vehicle()

@api.route('/get-vehicle/<int:id>', methods=['GET'])
def get_vehicle_by_id_route(id):
    return fonction.get_vehicle_by_id(id)

@api.route('/vehicules', methods=['POST'])
def add_vehicule_route():
    return fonction.add_vehicule()

@api.route('/devis/<int:vehicule_id>', methods=['POST'])
def save_devis_route(vehicule_id):
    return fonction.save_devis(vehicule_id)

@api.route('/filter-vehicles', methods=['GET'])
def filter_vehicles_route():
    return fonction.filter_vehicles()

@api.route('/update-etat-vehicule', methods=['PUT'])
def update_etat_vehicule_route():
    return fonction.update_etat_vehicule()

@api.route('/get-achat-vehicule', methods=['GET'])
def get_achat_vehicule_route():
    return fonction.get_achat_vehicule()

@api.route('/get-louer-vehicule', methods=['GET'])
def get_louer_vehicule_route():
    return fonction.get_louer_vehicule()

@api.route('/vehicules/filter', methods=['POST'])
def filter_vehicules_route():
    return fonction.filter_vehicules()

@api.route('/marques', methods=['GET'])
def get_marques_route():
    return fonction.get_marques()

@api.route('/modeles/<marque>', methods=['GET'])
def get_modeles_route(marque):
    return fonction.get_modeles(marque)

@api.route('/upload-images', methods=['POST'])
def upload_images_route():
    return fonction.upload_images()

@api.route('/upload-devis', methods=['POST', 'OPTIONS'])
def upload_devis_route():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 200
    return fonction.upload_devis()

@api.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

@api.route('/me', methods=['GET'])
def get_user_profile():
    return fonction.get_user_profile()

@api.route('/user/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    return fonction.get_user_details(user_id)

# Enregistrer le blueprint
app.register_blueprint(api)

# Configuration du logging
if not app.debug:
    file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')

@app.route('/api/get-louer-vehicule', methods=['GET'])
def louer_vehicule():
    return get_louer_vehicule()

@app.route('/api/update-etat-vehicule', methods=['PUT'])
def update_etat_vehicule_route():
    return update_etat_vehicule()

if __name__ == "__main__":
    logging.info("Starting Flask application...")
    app.run(host="0.0.0.0", port=8000, debug=True)

