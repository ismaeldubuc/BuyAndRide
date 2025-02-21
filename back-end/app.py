import psycopg2
import psycopg2.extras
from flask import Flask, request, jsonify, send_from_directory, Blueprint
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from fonction import register, login, profile, logout, create_vehicle, update_vehicle, delete_vehicle, get_vehicle , save_devis,list_vehicules,get_vehicule,add_vehicule,get_vehicle_by_id,update_etat_vehicule,get_achat_vehicule, get_louer_vehicule,filter_vehicules,get_marques,get_modeles, modif_profil,check_login
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
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/login', methods=['POST'])
def login_route():
    return login()

@api.route('/register', methods=['POST'])
def register_route():
    return register()

@api.route('/logout', methods=['POST'])
def logout_route():
    return logout()

@api.route('/modif_profil', methods=['POST'])
def modif_profil_route():
    return modif_profil()

CORS(app, resources={r"/*": {
    "origins": [
        "https://main.d3bzhfj3yrtaed.amplifyapp.com",
        "https://amplify.d3bzhfj3yrtaed.amplifyapp.com"
    ],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
    "supports_credentials": True,
    "expose_headers": ["Content-Type", "Authorization"],
    "max_age": 600,
    "allow_redirects": True
}})

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD')
)
Session(app)

Talisman(app, 
    content_security_policy={
        'default-src': "'self'",
        'img-src': ['*', 'data:', 'https:'],
        'script-src': ["'self'", "'unsafe-inline'"],
        'style-src': ["'self'", "'unsafe-inline'"]
    }
)

Compress(app)

# Configuration de la connexion à PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('PG_HOST', 'hetic.cd5ufp6fsve3.us-east-1.rds.amazonaws.com'),
            port=os.getenv('PG_PORT', '5432'),
            database=os.getenv('PG_DB', 'groupe4'),
            user=os.getenv('PG_USER', 'postgres'),
            password=os.getenv('PG_PASSWORD', 'LeContinent!')
        )
        logging.info("Database connection successful")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {str(e)}")
        raise

@app.route("/")
def home():
    return "Hello, World!"

# Routes
@api.route('/login', methods=['POST'])
def login_route():
    return login()

@app.route('/check-login', methods=['GET'])
def check_login_route():
    return check_login()

@api.route('/register', methods=['POST'])
def register_route():
    return register()

@api.route('/profile', methods=['GET'])
def profile_route():
    return profile()

@api.route("/create-vehicle", methods=["POST"])
def create_vehicle_func():
    return create_vehicle()

@api.route('/vehicules', methods=['GET'])
def list_vehicules_route():
    return list_vehicules()

@api.route('/vehicules/<int:id>', methods=['GET'])
def get_vehicule_route(id):
    return get_vehicule(id)

@api.route('/static/uploads/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/uploads', filename)

@api.route("/update-vehicle", methods=["PUT"])
def update_vehicle_func():
    return update_vehicle()

@api.route("/delete-vehicle", methods=["DELETE"])
def delete_vehicle_func():
    return delete_vehicle()

@api.route("/get-vehicle", methods=["GET"])
def get_vehicle_func():
    return get_vehicle()

@api.route("/get-vehicle/<int:id>", methods=["GET"])
def get_vehicle_by_id_func(id):
    return get_vehicle_by_id(id)

@api.route('/vehicules', methods=['POST'])
def add_vehicule_route():
   return add_vehicule()

@api.route('/devis/<int:vehicule_id>', methods=['POST'])
def save_devis_route(vehicule_id):
    if not request.data:
        return jsonify({"error": "Aucune donnée PDF fournie"}), 400
    return save_devis(vehicule_id, request.data)

@api.route("/filter-vehicles", methods=["GET"])
def filter_vehicles_func():
    return filter_vehicles()

@api.route('/update-etat-vehicule', methods=['PUT'])
def update_etat_vehicule_route():
    return update_etat_vehicule()

@api.route('/get-achat-vehicule', methods=['GET'])
def get_achat_vehicule_route():
    return get_achat_vehicule()

@api.route('/get-louer-vehicule', methods=['GET'])
def get_louer_vehicule_route():
    return get_louer_vehicule()

@api.route('/vehicules/filter', methods=['POST'])
def filter_vehicules_route():
    return filter_vehicules()

@api.route('/marques', methods=['GET'])
def get_marques_route():
    return get_marques()

@api.route('/modeles/<marque>', methods=['GET'])
def get_modeles_route(marque):
    return get_modeles(marque)

s3_client = boto3.client('s3')
BUCKET_NAME = 'votre-bucket-s3'

def upload_file_to_s3(file, filename):
    try:
        s3_client.upload_fileobj(
            file,
            BUCKET_NAME,
            filename,
            ExtraArgs={'ACL': 'public-read'}
        )
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
    except ClientError as e:
        print(e)
        return None

@api.errorhandler(Exception)
def handle_error(error):
    response = {
        "error": str(error),
        "message": "Une erreur s'est produite sur le serveur."
    }
    if hasattr(error, 'code'):
        return jsonify(response), error.code
    return jsonify(response), 500

@api.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@api.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "error": "Not Found",
        "message": "La ressource demandée n'existe pas"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "Une erreur interne s'est produite"
    }), 500

if not app.debug:
    file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')

app.register_blueprint(api)

if __name__ == "__main__":
    logging.info("Starting Flask application...")
    app.run(host="0.0.0.0", port=8000, debug=True)
