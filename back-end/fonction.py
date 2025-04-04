import time
from flask import Flask, request, jsonify, session as flask_session, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt_identity
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from pdf_handler import extract_text_from_files_in_folder
from ollama_handler import ask_ollama
import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv
from flask_cors import CORS
import time
import json
from database import get_db_connection
import logging
from botocore.exceptions import ClientError
from botocore.config import Config
import boto3

load_dotenv()

# Au début du fichier, après load_dotenv()
print("AWS Credentials:", {
    'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
    'AWS_REGION': os.getenv('AWS_REGION')
})

# Créer une instance de Flask et Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)

# Définir le dossier d'upload
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Extensions autorisées
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Configure CORS
CORS(app, resources={r"/api/*": {
    "origins": "http://localhost:5173",  # Spécifiez ici l'origine exacte de votre front-end
    "methods": ["GET", "POST", "PUT", "DELETE"],  # Les méthodes HTTP autorisées
    "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],  # Les en-têtes autorisés
    "supports_credentials": True  # Permet les cookies cross-origin, les en-têtes d'autorisation, etc.
}})

# Configuration S3
s3_client = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_vehicle():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO vehicules (marque, modele, prix, km, energie, photo1, photo2, photo3, photo4, photo5, etat, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data['marque'], data['modele'], data['prix'], data['km'], data['energie'],
                               data['photo1'], data['photo2'], data['photo3'], data['photo4'], data['photo5'],
                               data['etat'], data['description']))
        conn.commit()
        return jsonify({"message": "Vehicle created successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

def update_vehicle():
    data = request.json
    vehicle_id = data.get('id')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE vehicules 
            SET marque = %s, modele = %s, prix = %s, km = %s, 
                energie = %s, photo1 = %s, photo2 = %s,
                photo3 = %s, photo4 = %s, photo5 = %s, etat = %s, description = %s
            WHERE id = %s
        """
        cursor.execute(query, (data['marque'], data['modele'], data['prix'], data['km'],
                               data['energie'], data['photo1'], data['photo2'],
                               data['photo3'], data['photo4'], data['photo5'],
                               data['etat'], data['description'], vehicle_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Vehicle not found"}), 404
        return jsonify({"message": "Vehicle updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

def delete_vehicle():
    data = request.json
    vehicle_id = data.get('id')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM vehicules WHERE id = %s"
        cursor.execute(query, (vehicle_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Vehicle not found"}), 404
        return jsonify({"message": "Vehicle deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

def get_vehicle():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        query = "SELECT * FROM vehicules"
        cursor.execute(query)
        vehicles = cursor.fetchall()
        return jsonify(vehicles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        
def get_vehicule_by_id(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        # Requête modifiée pour utiliser la table uservehicule
        query = """
            SELECT v.*, u.nom as vendeur_nom, u.prenom as vendeur_prenom 
            FROM vehicules v 
            LEFT JOIN uservehicule uv ON v.id = uv.id_vehicule
            LEFT JOIN users u ON uv.id_user = u.id
            WHERE v.id = %s
        """
        
        cursor.execute(query, (id,))
        vehicule = cursor.fetchone()
        
        if not vehicule:
            return jsonify({"error": "Véhicule non trouvé"}), 404
            
        # Convertir en dictionnaire
        vehicule_dict = dict(vehicule)
        
        # Convertir les valeurs Decimal en float pour la sérialisation JSON
        if 'prix' in vehicule_dict:
            vehicule_dict['prix'] = float(vehicule_dict['prix'])
            
        # Ne pas modifier les URLs S3
        # Les images sont déjà des URLs S3 complètes

        return jsonify(vehicule_dict)

    except Exception as e:
        print(f"Erreur dans get_vehicule_by_id: {str(e)}")  # Pour le débogage
        return jsonify({
            "error": str(e),
            "message": "Erreur lors de la récupération du véhicule",
            "details": {
                "id": id,
                "error_type": type(e).__name__,
                "error_args": e.args
            }
        }), 500
    finally:
        if 'cursor' in locals():
        cursor.close()
        if 'conn' in locals():
        conn.close()

def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Données JSON manquantes"}), 400
            
        nom = data.get('nom')
        prenom = data.get('prenom')
        email = data.get('email')
        password = data.get('password')

        if not all([nom, prenom, email, password]):
            return jsonify({"message": "Tous les champs sont requis"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        # Vérifier si l'email existe déjà
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"message": "Cet email est déjà utilisé"}), 409
            
        # Hasher le mot de passe
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Insérer le nouvel utilisateur
        cursor.execute(
            "INSERT INTO users (nom, prenom, email, mdp) VALUES (%s, %s, %s, %s)",
            (nom, prenom, email, hashed_password)
        )
            conn.commit()
        
            return jsonify({"message": "Inscription réussie"}), 201
        
        except Exception as e:
        return jsonify({"message": f"Erreur serveur: {str(e)}"}), 500
        finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def login():
    try:
    data = request.get_json()
        if not data:
            return jsonify({"message": "Données JSON manquantes"}), 400
            
    email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"message": "Email et mot de passe requis"}), 400
            
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user and bcrypt.check_password_hash(user['mdp'], password):
            flask_session.clear()
            flask_session['user_id'] = user['id']
            access_token = create_access_token(identity=user['id'])
            return jsonify({
                "message": "Connexion réussie",
                "token": access_token
            }), 200
        return jsonify({"message": "Identifiants incorrects"}), 401
    except Exception as e:
        return jsonify({"message": f"Erreur serveur: {str(e)}"}), 500
    finally:
        if 'cursor' in locals():
        cursor.close()
        if 'conn' in locals():
        conn.close()

import logging

logging.basicConfig(level=logging.DEBUG)
    
def check_login():
    try:
        if 'user_id' in flask_session:
            return jsonify({
                "isLoggedIn": True,
                "user_id": flask_session['user_id']
            }), 200
        return jsonify({"isLoggedIn": False}), 200
    except Exception as e:
        print(f"Erreur dans check_login: {str(e)}")
        return jsonify({"error": str(e)}), 500

def profile():
    try:
        if 'user_id' not in flask_session:
            return jsonify({"error": "Utilisateur non connecté"}), 401

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)

        cursor.execute("SELECT nom, prenom, email FROM users WHERE id = %s", (flask_session['user_id'],))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "Utilisateur non trouvé"}), 404

        return jsonify([user['nom'], user['prenom'], user['email']]), 200

    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500
    finally:
        if 'cursor' in locals():
        cursor.close()
        if 'conn' in locals():
        conn.close()

def modif_profil():
    try:
        if 'user_id' not in flask_session:
            return jsonify({"error": "Utilisateur non connecté"}), 401

        data = request.get_json()
        if not data:
            return jsonify({"error": "Données manquantes"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Construction de la requête de mise à jour
        update_fields = []
        params = []
        
        if 'nom' in data and data['nom']:
            update_fields.append("nom = %s")
            params.append(data['nom'])
        if 'prenom' in data and data['prenom']:
            update_fields.append("prenom = %s")
            params.append(data['prenom'])
        if 'email' in data and data['email']:
            update_fields.append("email = %s")
            params.append(data['email'])
        if 'password' in data and data['password']:
            update_fields.append("mdp = %s")
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            params.append(hashed_password)

        if not update_fields:
            return jsonify({"error": "Aucune donnée à mettre à jour"}), 400

        params.append(flask_session['user_id'])
        query = f"""
            UPDATE users 
            SET {', '.join(update_fields)}
            WHERE id = %s
        """

        cursor.execute(query, tuple(params))
                conn.commit()

                return jsonify({"message": "Profil mis à jour avec succès"}), 200

    except Exception as e:
        print(f"Erreur dans modif_profil: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
        cursor.close()
        if 'conn' in locals():
        conn.close()

def logout():
    try:
        # Effacer la session
        flask_session.clear()
    return jsonify({"message": "Déconnexion réussie"}), 200
    except Exception as e:
        print(f"Erreur dans logout: {str(e)}")
        return jsonify({"error": str(e)}), 500

def list_vehicules():
    if 'user_id' not in flask_session:
        return jsonify({"error": "Authentication required"}), 401
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute("SELECT * FROM vehicules WHERE user_id = %s", (flask_session['user_id'],))
        vehicules = cursor.fetchall()
        return jsonify(vehicules)
    finally:
        cursor.close()
        conn.close()

def add_vehicule():
    try:
        if 'user_id' not in flask_session:
            return jsonify({"error": "Utilisateur non connecté"}), 401

        data = request.get_json()
        if not data:
            return jsonify({"error": "Données manquantes"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insérer d'abord le véhicule
        query = """
            INSERT INTO vehicules (marque, modele, prix, km, energie, type, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """

        cursor.execute(query, (
            data['marque'],
            data['modele'],
            data['prix'],
            data['km'],
            data['energie'],
            data['type'],
            data['description']
        ))

        vehicule_id = cursor.fetchone()[0]

        # Insérer dans la table uservehicule
        query_user_vehicule = """
            INSERT INTO uservehicule (id_user, id_vehicule)
            VALUES (%s, %s)
        """
        
        cursor.execute(query_user_vehicule, (flask_session['user_id'], vehicule_id))
        conn.commit()

        return jsonify({
            "message": "Véhicule ajouté avec succès",
            "id": vehicule_id
        }), 201

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Erreur dans add_vehicule: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Erreur lors de l'ajout du véhicule"
        }), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_vehicule(id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute("SELECT v.*, u.nom as vendeur_nom, u.prenom as vendeur_prenom FROM vehicules v JOIN users u ON v.user_id = u.id WHERE v.id = %s", (id,))
        vehicule = cursor.fetchone()
        if vehicule is None:
            return jsonify({"error": "Vehicle not found"}), 404
        return jsonify(vehicule)
    finally:
        cursor.close()
        conn.close()

def save_file(file_key):
    file = request.files.get(file_key)
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        absolute_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(absolute_path)
        return os.path.join('uploads', filename)
    return None

def save_devis(vehicule_id, pdf_data):
    if 'user_id' not in flask_session:
        return jsonify({"error": "Authentification requise"}), 401
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        devis_path = os.path.join(app.config['UPLOAD_FOLDER'], 'devis')
        if not os.path.exists(devis_path):
            os.makedirs(devis_path)
        filename = f"devis_{vehicule_id}_{flask_session['user_id']}_{int(time.time())}.pdf"
        file_path = os.path.join(devis_path, filename)
        with open(file_path, 'wb') as f:
            f.write(pdf_data)
        sql = "INSERT INTO devis_pdf (user_id, vehicule_id, pdf_path) VALUES (%s, %s, %s)"
        cursor.execute(sql, (flask_session['user_id'], vehicule_id, os.path.join('uploads/devis', filename)))
        conn.commit()
        return jsonify({"message": "Devis enregistré avec succès", "pdf_path": os.path.join('uploads/devis', filename)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def filter_vehicles():
    try:
        marque = request.args.get('marque')
        modele = request.args.get('modele')
        energie = request.args.get('energie')
        prix_max = request.args.get('prix')
        km_max = request.args.get('km')
        type_vehicule = request.args.get('type')

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        query = """
            SELECT *
            FROM vehicules 
            WHERE 1=1
        """
        params = []

        if type_vehicule:
            query += " AND type = %s"
            params.append(type_vehicule == 'true')

        if marque:
            query += " AND marque = %s"
            params.append(marque)
        
        if modele:
            query += " AND modele = %s"
            params.append(modele)
            
        if energie:
            query += " AND energie = %s"
            params.append(energie)
            
        if prix_max:
            query += " AND prix <= %s"
            params.append(float(prix_max))
            
        if km_max:
            query += " AND km <= %s"
            params.append(int(km_max))

        cursor.execute(query, tuple(params))
        vehicles = cursor.fetchall()

        # Convertir les résultats
        vehicles_list = []
        for vehicle in vehicles:
            vehicle_dict = dict(vehicle)
            if 'prix' in vehicle_dict:
                vehicle_dict['prix'] = float(vehicle_dict['prix'])
            for i in range(1, 6):
                photo_key = f'photo{i}'
                if vehicle_dict.get(photo_key):
                    vehicle_dict[photo_key] = os.path.join('uploads', os.path.basename(vehicle_dict[photo_key]))
            vehicles_list.append(vehicle_dict)
        
        return jsonify(vehicles_list)

    except Exception as e:
        print(f"Erreur dans filter_vehicles: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_vehicules():
    try:
        # Vérifier si l'utilisateur est connecté
        if 'user_id' not in flask_session:
            return jsonify({"error": "Utilisateur non connecté"}), 401

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        # Modifier la requête pour utiliser la table uservehicule
        query = """
            SELECT v.* 
            FROM vehicules v
            JOIN uservehicule uv ON v.id = uv.id_vehicule
            WHERE uv.id_user = %s
        """
        
        cursor.execute(query, (flask_session['user_id'],))
        vehicles = cursor.fetchall()

        vehicles_list = []
        for vehicle in vehicles:
            vehicle_dict = dict(vehicle)
            # Convertir les valeurs Decimal en float pour la sérialisation JSON
            if 'prix' in vehicle_dict:
                vehicle_dict['prix'] = float(vehicle_dict['prix'])
            # Ne pas modifier les URLs des images
            vehicles_list.append(vehicle_dict)

        return jsonify(vehicles_list)

    except Exception as e:
        logging.error(f"Error in get_vehicules: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Erreur lors de la récupération des véhicules"
        }), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_louer_vehicule():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        query = """
            SELECT * 
            FROM vehicules 
            WHERE type = false
        """
        
        cursor.execute(query)
        vehicules = cursor.fetchall()

        vehicules_list = []
        for vehicule in vehicules:
            vehicule_dict = dict(vehicule)
            if 'prix' in vehicule_dict:
                vehicule_dict['prix'] = float(vehicule_dict['prix'])
            # Ne pas modifier les URLs S3
            vehicules_list.append(vehicule_dict)

        return jsonify(vehicules_list)

    except Exception as e:
        print(f"Erreur dans get_louer_vehicule: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Erreur lors de la récupération des véhicules à louer"
        }), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_achat_vehicule():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        query = """
            SELECT * 
            FROM vehicules 
            WHERE type = true
        """
        
        cursor.execute(query)
        vehicules = cursor.fetchall()

        vehicules_list = []
        for vehicule in vehicules:
            vehicule_dict = dict(vehicule)
            if 'prix' in vehicule_dict:
                vehicule_dict['prix'] = float(vehicule_dict['prix'])
            # Ne pas modifier les URLs S3
            vehicules_list.append(vehicule_dict)

        return jsonify(vehicules_list)

    except Exception as e:
        print(f"Erreur dans get_achat_vehicule: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Erreur lors de la récupération des véhicules à vendre"
        }), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def upload_to_s3(file, filename):
    """Upload un fichier vers S3 et retourne son URL"""
    try:
        bucket_name = os.getenv('S3_BUCKET')
        s3_client.upload_fileobj(
            file,
            bucket_name,
            f'vehicules/{filename}',
            ExtraArgs={
                'ContentType': file.content_type
            }
        )
        return f"https://{bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/vehicules/{filename}"
    except ClientError as e:
        print(f"Erreur S3: {str(e)}")
        return None

def upload_images():
    try:
        vehicule_id = request.form.get('vehicule_id')
        if not vehicule_id:
            return jsonify({"error": "ID du véhicule manquant"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Traitement des images
        updates = []
        params = []
        for i in range(1, 6):
            if f'photo{i}' in request.files:
                file = request.files[f'photo{i}']
                if file and file.filename and allowed_file(file.filename):
                    # Générer un nom de fichier unique
                    filename = secure_filename(f"{vehicule_id}_{i}_{file.filename}")
                    
                    # Upload vers S3
                    s3_url = upload_to_s3(file, filename)
                    if s3_url:
                        updates.append(f"photo{i} = %s")
                        params.append(s3_url)
                    else:
                        return jsonify({"error": f"Erreur lors de l'upload de l'image {i} vers S3"}), 500

        if updates:
            query = f"""
                UPDATE vehicules 
                SET {', '.join(updates)}
                WHERE id = %s
            """
            params.append(vehicule_id)
            cursor.execute(query, tuple(params))
            conn.commit()

        return jsonify({"message": "Images uploadées avec succès"}), 200

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Erreur dans upload_images: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def upload_pdf_to_s3(pdf_data, filename):
    try:
        bucket_name = os.getenv('S3_BUCKET')
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f'devis/{filename}',
            Body=pdf_data,
            ContentType='application/pdf'
        )
        return f"https://{bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/devis/{filename}"
    except Exception as e:
        print(f"Erreur lors de l'upload du PDF vers S3: {str(e)}")
        return None

def chat():
    try:
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({"error": "Aucune question fournie"}), 400
        
        # Extraire le texte des PDFs de S3
        try:
            # Créer un dossier temporaire pour les PDFs
            temp_folder = os.path.join('static', 'temp_pdfs')
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
            
            # Télécharger les PDFs de S3
            bucket_name = os.getenv('S3_BUCKET')
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='devis/')
            
            if 'Contents' in response:
                for obj in response['Contents']:
                    if obj['Key'].endswith('.pdf'):
                        local_path = os.path.join(temp_folder, os.path.basename(obj['Key']))
                        s3_client.download_file(bucket_name, obj['Key'], local_path)
            
            # Extraire le texte des PDFs
            context = extract_text_from_files_in_folder(temp_folder)
            
            # Nettoyer le dossier temporaire
            for file in os.listdir(temp_folder):
                os.remove(os.path.join(temp_folder, file))
            os.rmdir(temp_folder)
            
        except Exception as e:
            print(f"Erreur lors de l'extraction des PDFs: {str(e)}")
            context = "Aucun PDF trouvé dans S3."
        
        # Appeler la fonction ask_ollama avec la question et le contexte
        response = ask_ollama(question, context)
        
        return jsonify({"response": response}), 200
    except Exception as e:
        print(f"Erreur dans chat: {str(e)}")
        return jsonify({"error": str(e)}), 500

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

def upload_devis():
    try:
        if 'user_id' not in flask_session:
            return jsonify({"error": "Utilisateur non connecté"}), 401

        # Récupérer le fichier PDF et l'ID du véhicule depuis le formulaire
        if 'pdf' not in request.files:
            return jsonify({"error": "Aucun fichier PDF fourni"}), 400
            
        pdf_file = request.files['pdf']
        vehicule_id = request.form.get('vehicule_id')
        
        if not vehicule_id:
            return jsonify({"error": "ID du véhicule manquant"}), 400

        # Générer un nom de fichier unique pour le devis
        filename = f"devis_{vehicule_id}_{flask_session['user_id']}_{int(time.time())}.pdf"
        
        # Upload vers S3
        s3_url = upload_pdf_to_s3(pdf_file.read(), filename)
        if not s3_url:
            return jsonify({"error": "Erreur lors de l'upload du devis vers S3"}), 500

        # Enregistrer dans la base de données
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO pdf (id_vehicule, id_user, pdf, description)
                VALUES (%s, %s, %s, %s)
            """, (vehicule_id, flask_session['user_id'], s3_url, "Devis généré automatiquement"))
            conn.commit()
            return jsonify({
                "message": "Devis enregistré avec succès",
                "url": s3_url
            }), 201
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Erreur dans upload_devis: {str(e)}")
        return jsonify({"error": str(e)}), 500
