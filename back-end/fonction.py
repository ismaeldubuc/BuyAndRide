from flask import Flask, request, jsonify, session, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv
from flask_cors import CORS
import time

load_dotenv()

app = Flask(__name__)
app.secret_key = 'buyandride'
bcrypt = Bcrypt(app)

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

app = Flask(__name__)
# Configure CORS
CORS(app, resources={r"/api/*": {
    "origins": "http://localhost:5173",  # Spécifiez ici l'origine exacte de votre front-end
    "methods": ["GET", "POST", "PUT", "DELETE"],  # Les méthodes HTTP autorisées
    "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],  # Les en-têtes autorisés
    "supports_credentials": True  # Permet les cookies cross-origin, les en-têtes d'autorisation, etc.
}})


def get_db_connection():
    conn = psycopg2.connect(
        host='hetic.cd5ufp6fsve3.us-east-1.rds.amazonaws.com',
        port='5432',
        database='groupe4',
        user='postgres',
        password='LeContinent!'  # Utiliser dotenv pour le mot de passe en production
    )
    return conn

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
        
def get_vehicle_by_id(id):
    cursor = db.cursor(dictionary=True)

    try:
        query = """
            SELECT * 
            FROM vehicules
            WHERE id = %s
        """
        cursor.execute(query, (id,))
        vehicle = cursor.fetchone()

        return jsonify(vehicle), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()

def register():
    if request.method == 'POST':
        data = request.json
        nom = data.get('nom')
        prenom = data.get('prenom')
        email = data.get('email')
        password = data.get('password')

        # Utilisation de la méthode correcte pour générer le hash du mot de passe
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (nom, prenom, email, mdp) VALUES (%s, %s, %s, %s)", (nom, prenom, email, password_hash))
            conn.commit()
            return jsonify({"message": "Inscription réussie"}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400
        finally:
            cursor.close()
            conn.close()


def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')  # Assurez-vous que ceci correspond au nom de champ utilisé dans votre JSON de requête
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and bcrypt.check_password_hash(user['mdp'], password):  # Utilisez la méthode correcte ici
            session['user_id'] = user['id']
            return jsonify({"message": "Connexion réussie"}), 200
        return jsonify({"message": "Identifiants incorrects"}), 401
    finally:
        cursor.close()
        conn.close()


def profile():
    if 'user_id' not in session:
        return jsonify({"error": "Utilisateur non authentifié"}), 401
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        if request.method == 'GET':
            cursor.execute("SELECT nom, prenom, email FROM users WHERE id = %s", (session['user_id'],))
            user = cursor.fetchone()
            return jsonify(user)
        elif request.method == 'POST':
            data = request.get_json()
            new_mdp = data.get('new_mdp')
            confirm_mdp = data.get('confirm_mdp')
            if new_mdp != confirm_mdp:
                return jsonify({"error": "Les mots de passe ne correspondent pas"}), 400
            new_mdp_hash = bcrypt.generate_mdp_hash(new_mdp).decode('utf-8')
            cursor.execute("UPDATE users SET mdp = %s WHERE id = %s", (new_mdp_hash, session['user_id']))
            conn.commit()
            return jsonify({"message": "Mot de passe mis à jour avec succès"}), 200
    finally:
        cursor.close()
        conn.close()

def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Déconnexion réussie"}), 200

def list_vehicules():
    if 'user_id' not in session:
        return jsonify({"error": "Authentication required"}), 401
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute("SELECT * FROM vehicules WHERE user_id = %s", (session['user_id'],))
        vehicules = cursor.fetchall()
        return jsonify(vehicules)
    finally:
        cursor.close()
        conn.close()

def add_vehicule():
    if 'user_id' not in session:
        return jsonify({"error": "Authentication required"}), 401
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO vehicules (user_id, marque, modele, prix, kilometrage, energie, type, description, photo1, photo2, photo3, photo4, photo5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (session['user_id'], data['marque'], data['modele'], data['prix'], data['kilometrage'], data['energie'], data['type'], data['description'], data['photo1'], data['photo2'], data['photo3'], data['photo4'], data['photo5'])
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"message": "Vehicle added successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
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
    if 'user_id' not in session:
        return jsonify({"error": "Authentification requise"}), 401
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        devis_path = os.path.join(app.config['UPLOAD_FOLDER'], 'devis')
        if not os.path.exists(devis_path):
            os.makedirs(devis_path)
        filename = f"devis_{vehicule_id}_{session['user_id']}_{int(time.time())}.pdf"
        file_path = os.path.join(devis_path, filename)
        with open(file_path, 'wb') as f:
            f.write(pdf_data)
        sql = "INSERT INTO devis_pdf (user_id, vehicule_id, pdf_path) VALUES (%s, %s, %s)"
        cursor.execute(sql, (session['user_id'], vehicule_id, os.path.join('uploads/devis', filename)))
        conn.commit()
        return jsonify({"message": "Devis enregistré avec succès", "pdf_path": os.path.join('uploads/devis', filename)}), 201
    except Exception as e:
        return jsonify({"error": str
                        (e)}), 500

def filter_vehicules():
    marque = request.args.get('marque')
    modele = request.args.get('modele')
    prix = request.args.get('prix')
    kilometrage = request.args.get('kilometrage')
    energie = request.args.get('energie')
    type_vehicule = request.args.get('type')

    cursor = db.cursor(dictionary=True)
    
    query = "SELECT * FROM vehicules WHERE 1=1"
    params = []

    if marque:
        query += " AND marque = %s"
        params.append(marque)
    
    if modele:
        query += " AND modele = %s" 
        params.append(modele)

    if prix:
        query += " AND prix <= %s"
        params.append(prix)

    if kilometrage:
        query += " AND km <= %s"
        params.append(kilometrage)

    if energie:
        query += " AND energie = %s"
        params.append(energie)

    if type_vehicule:
        query += " AND type = %s"
        params.append(type_vehicule)

    try:
        cursor.execute(query, params)
        vehicules = cursor.fetchall()
        response = {"vehicules": vehicules}
        if type_vehicule:
            response["type"] = type_vehicule
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
    
def update_etat_vehicule():
    data = request.json
    vehicule_id = data.get('id')
    etat = data.get('etat')
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE vehicules SET etat = %s WHERE id = %s", (etat, vehicule_id))
        db.commit()
        return jsonify({"message": "Etat du véhicule mis à jour avec succès"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()

def get_achat_vehicule():
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM vehicules WHERE etat = 'true'")
        vehicules_achetes = cursor.fetchall()
        return jsonify(vehicules_achetes), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()

def get_louer_vehicule():
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM vehicules WHERE etat = 'false'")
        vehicules_loues = cursor.fetchall()
        return jsonify(vehicules_loues), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
    
def get_marques():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DISTINCT marque FROM vehicules ORDER BY marque")
        marques = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return jsonify(marques)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_modeles(marque):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DISTINCT modele FROM vehicules WHERE marque = %s ORDER BY modele", (marque,))
        modeles = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return jsonify(modeles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def filter_vehicles():
    try:
        # Récupérer les paramètres de filtrage depuis l'URL
        marque = request.args.get('marque')
        modele = request.args.get('modele')
        energie = request.args.get('energie')
        prix_max = request.args.get('prix')
        km_max = request.args.get('kilometrage')

        cursor = db.cursor(dictionary=True)
        
        # Construction de la requête de base
        query = """
            SELECT v.*, u.nom as vendeur_nom, u.prenom as vendeur_prenom
            FROM vehicules v 
            JOIN users u ON v.user_id = u.id 
            WHERE 1=1
        """
        params = []

        # Ajout des conditions de filtrage
        if marque:
            query += " AND v.marque = %s"
            params.append(marque)
        
        if modele:
            query += " AND v.modele = %s"
            params.append(modele)
            
        if energie:
            query += " AND v.energie = %s"
            params.append(energie)
            
        if prix_max:
            query += " AND v.prix <= %s"
            params.append(float(prix_max))
            
        if km_max:
            query += " AND v.kilometrage <= %s"
            params.append(int(km_max))

        cursor.execute(query, tuple(params))
        vehicles = cursor.fetchall()

        # Transformation des chemins d'images pour correspondre à votre structure
        for vehicle in vehicles:
            for i in range(1, 6):
                photo_key = f'photo{i}'
                if vehicle.get(photo_key):
                    vehicle[photo_key] = os.path.join('uploads', os.path.basename(vehicle[photo_key]))
        
        return jsonify(vehicles)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
