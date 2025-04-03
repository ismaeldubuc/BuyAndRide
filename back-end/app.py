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

# Set up logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # Ajoutez une clé secrète pour JWT

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

api = Blueprint('api', __name__, url_prefix='/api')

# Configuration CORS correcte
CORS(app, 
    resources={
        r"/api/*": {
            "origins": ["http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    }
)

# Configuration de la session
if os.getenv('FLASK_ENV') == 'production':
    # Configuration Redis pour la production
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = Redis(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        password=os.getenv('REDIS_PASSWORD')
    )
else:
    # Configuration pour le développement local
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

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
    return fonction.create_vehicle()

@api.route('/vehicules', methods=['GET'])
def get_vehicules_route():
    return fonction.get_vehicules()

@api.route('/vehicules/<int:id>', methods=['GET'])
def get_vehicle(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        query = """
            SELECT * 
            FROM vehicules 
            WHERE id = %s
        """
        
        cursor.execute(query, (id,))
        vehicule = cursor.fetchone()

        if not vehicule:
            return jsonify({"error": "Véhicule non trouvé"}), 404

        vehicule_dict = dict(vehicule)
        if 'prix' in vehicule_dict:
            vehicule_dict['prix'] = float(vehicule_dict['prix'])

        return jsonify(vehicule_dict)

    except Exception as e:
        print(f"Erreur dans get_vehicle: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Erreur lors de la récupération du véhicule"
        }), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@api.route('/static/uploads/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/uploads', filename)

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
    try:
        return fonction.get_vehicle_by_id(id)
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Erreur lors de la récupération du véhicule"
        }), 500

@api.route('/vehicules', methods=['POST'])
def add_vehicule_route():
   return fonction.add_vehicule()

@api.route('/devis/<int:vehicule_id>', methods=['POST'])
def save_devis_route(vehicule_id):
    if not request.data:
        return jsonify({"error": "Aucune donnée PDF fournie"}), 400
    return fonction.save_devis(vehicule_id, request.data)

@api.route('/filter-vehicles', methods=['GET'])
def filter_vehicles_route():
    try:
        return fonction.filter_vehicles()
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Erreur lors du filtrage des véhicules"
        }), 500

@api.route('/update-etat-vehicule', methods=['PUT'])
def update_etat_vehicule_route():
    return fonction.update_etat_vehicule()

@api.route('/get-achat-vehicule', methods=['GET'])
def get_achat_vehicule_route():
    try:
        return fonction.get_achat_vehicule()
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Erreur lors de la récupération des véhicules à vendre"
        }), 500

@api.route('/get-louer-vehicule', methods=['GET'])
def get_louer_vehicule_route():
    try:
        return fonction.get_louer_vehicule()
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Erreur lors de la récupération des véhicules à louer"
        }), 500

@api.route('/vehicules/filter', methods=['POST'])
def filter_vehicules_route():
    return fonction.filter_vehicles()

@api.route('/marques', methods=['GET'])
def get_marques_route():
    return fonction.get_marques()

@api.route('/modeles/<marque>', methods=['GET'])
def get_modeles_route(marque):
    return fonction.get_modeles(marque)

@api.route('/upload-images', methods=['POST'])
def upload_images_route():
    try:
        return fonction.upload_images()
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Erreur lors de l'upload des images"
        }), 500

@api.route('/logout', methods=['POST'])
def logout_route():
    return fonction.logout()

@api.route('/api/upload-devis', methods=['POST', 'OPTIONS'])
def upload_devis():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        if 'user_id' not in flask_session:
            return jsonify({"error": "Utilisateur non connecté"}), 401

        if 'pdf' not in request.files:
            return jsonify({"error": "Pas de fichier PDF"}), 400
            
        pdf_file = request.files['pdf']
        vehicule_id = request.form.get('vehicule_id')
        
        if not pdf_file or not vehicule_id:
            return jsonify({"error": "Données manquantes"}), 400

        # Récupérer les informations de l'utilisateur
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("SELECT nom FROM users WHERE id = %s", (flask_session['user_id'],))
        user = cursor.fetchone()
        
        # Récupérer les informations du véhicule
        cursor.execute("SELECT modele FROM vehicules WHERE id = %s", (vehicule_id,))
        vehicule = cursor.fetchone()
        
        # Créer le nom du fichier
        filename = f"{user['nom']}_{vehicule['modele']}.pdf"
        s3_url = upload_pdf_to_s3(pdf_file, filename)
        
        if s3_url:
            return jsonify({"url": s3_url}), 200
        else:
            return jsonify({"error": "Erreur lors de l'upload"}), 500
            
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Gestion des erreurs
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

@api.route('/me', methods=['GET'])
def get_user_profile():
    try:
        if 'user_id' not in flask_session:
            return jsonify({"error": "Utilisateur non connecté"}), 401

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        cursor.execute("""
            SELECT id, nom, prenom, email 
            FROM users 
            WHERE id = %s
        """, (flask_session['user_id'],))
        
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "Utilisateur non trouvé"}), 404

        return jsonify({
            "id": user['id'],
            "nom": user['nom'],
            "prenom": user['prenom'],
            "email": user['email']
        })

    except Exception as e:
        print(f"Erreur dans get_user_profile: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@api.route('/user/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    try:
        # Vérifier si l'utilisateur est connecté
        if 'user_id' not in flask_session:
            return jsonify({"error": "Utilisateur non connecté"}), 401
            
        # Vérifier si l'utilisateur demande ses propres informations
        if int(flask_session['user_id']) != user_id:
            return jsonify({"error": "Accès non autorisé"}), 403
            
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        cursor.execute("""
            SELECT id, nom, prenom, email 
            FROM users 
            WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "Utilisateur non trouvé"}), 404
            
        return jsonify({
            "id": user['id'],
            "nom": user['nom'],
            "prenom": user['prenom'],
            "email": user['email']
        })
        
    except Exception as e:
        print(f"Erreur dans get_user_details: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Enregistrement du Blueprint
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

# Ajout d'un gestionnaire pour les requêtes OPTIONS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/api/update-etat-vehicule', methods=['PUT'])
def update_etat_vehicule_route():
    return update_etat_vehicule()

if __name__ == "__main__":
    logging.info("Starting Flask application...")
    app.run(host="0.0.0.0", port=8000, debug=True)

