from flask import Flask, request, jsonify, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt_identity
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import mysql.connector
import os
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
app.secret_key = 'buyandride'  
bcrypt = Bcrypt(app)

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

CORS(app, 
     resources={r"/*": {
         "origins": "http://localhost:5173/",  # Votre URL frontend
         "supports_credentials": True,         
         "methods": ["GET", "POST", "OPTIONS","PUT","DELETE"],
         "allow_headers": ["Content-Type", "Authorization"]
     }})

db = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DB')
)

def create_vehicle():
    data = request.json
    cursor = db.cursor()

    try:
        query = """
            INSERT INTO vehicules (marque, modele, prix, km, energie, photo1, photo2, photo3, photo4, photo5, etat, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data.get('marque'),
            data.get('modele'), 
            data.get('prix'),
            data.get('km'),
            data.get('energie'),
            data.get('photo1'),
            data.get('photo2'),
            data.get('photo3'),
            data.get('photo4'),
            data.get('photo5'),
            data.get('etat'),
            data.get('description')
        )

        cursor.execute(query, values)
        db.commit()

        return jsonify({"message": "Vehicle created successfully", "id": cursor.lastrowid}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()

def update_vehicle():
    data = request.json
    vehicle_id = data.get('id')
    
    cursor = db.cursor()

    try:
        query = """
            UPDATE vehicules 
            SET marque = %s, modele = %s, prix = %s, km = %s, 
                energie = %s, photo1 = %s, photo2 = %s,
                photo3 = %s, photo4 = %s, photo5 = %s, etat = %s, description = %s
            WHERE id = %s
        """
        values = (
            data.get('marque'),
            data.get('modele'),
            data.get('prix'), 
            data.get('km'),
            data.get('energie'),
            data.get('photo1'),
            data.get('photo2'),
            data.get('photo3'),
            data.get('photo4'),
            data.get('photo5'),
            data.get('etat'),
            data.get('description'),
            vehicle_id
        )

        cursor.execute(query, values)
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Vehicle not found"}), 404

        return jsonify({"message": "Vehicle updated successfully"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()

def delete_vehicle():
    data = request.json
    vehicle_id = data.get('id')

    cursor = db.cursor()

    try:
        query = "DELETE FROM vehicules WHERE id = %s"
        cursor.execute(query, (vehicle_id,))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Vehicle not found"}), 404

        return jsonify({"message": "Vehicle deleted successfully"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()

def get_vehicle():
    cursor = db.cursor(dictionary=True)

    try:
        query = """
            SELECT * 
            FROM vehicules
        """
        cursor.execute(query)
        vehicles = cursor.fetchall()

        return jsonify(vehicles), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

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

def register():
    if request.method == 'POST':
        data = request.json
        nom = data.get('nom')
        prenom = data.get('prenom')
        email = data.get('email')
        password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')

        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (nom, prenom, email, password) VALUES (%s, %s, %s, %s)", (nom, prenom, email, password))
            db.commit()
            return jsonify({"message": "Inscription réussie"}), 201  # Retourner une réponse JSON
        except mysql.connector.Error as err:
            return jsonify({"error": f"Erreur : {err}"}), 400

def login():
    data = request.get_json()  # Récupérer le JSON envoyé par le frontend
    email = data.get('email')
    password = data.get('password')

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user['password'], password):
        
        session['user_id'] = user['id']
        return jsonify({"message": "Connexion réussie"}), 200  # ✅ Retourne un JSON

    return jsonify({"message": "Identifiants incorrects"}), 401  # ✅ Retourne un JSON pour le frontend

def profile():
    """ Route pour afficher et modifier les informations de l'utilisateur """
    if 'user_id' not in session:
        return jsonify({"error": "Utilisateur non authentifié"}), 401
    
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT nom, prenom, email FROM users WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()
        return jsonify(user)
    if request.method == 'POST':
        if 'changer_mdp' in request.form:
            # Changement de mot de passe
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            if new_password != confirm_password:
                return jsonify({"error": "Les mots de passe ne correspondent pas"}), 400

            new_password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password_hash, session['user_id']))
            db.commit()
            return jsonify({"message": "Mot de passe mis à jour avec succès"}), 200

        else:
            # Modification des infos du profil
            nom = request.form.get('nom')
            prenom = request.form.get('prenom')
            email = request.form.get('email')

            cursor.execute("UPDATE users SET nom=%s, prenom=%s, email=%s WHERE id=%s", (nom, prenom, email, session['user_id']))
            db.commit()
            return jsonify({"message": "Profil mis à jour avec succès"}), 200

def logout():
    session.pop('user_id', None)  # Supprime l'utilisateur de la session
    return jsonify({"message": "Déconnexion réussie"}), 200

def list_vehicules():
    # Vérifie si l'utilisateur est connecté
    if 'user_id' not in session:
        return jsonify({"error": "Authentication required"}), 401

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vehicules WHERE user_id = %s", (session['user_id'],))
        vehicules = cursor.fetchall()
        return jsonify(vehicules)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def add_vehicule():
    if 'user_id' not in session:
        return jsonify({"error": "Authentication required"}), 401

    try:
        data = {
            'user_id': session['user_id'],
            'marque': request.form.get('marque'),
            'modele': request.form.get('modele'),
            'prix': request.form.get('prix'),
            'kilometrage': request.form.get('kilometrage'),
            'energie': request.form.get('energie'),
            'type': request.form.get('type'),
            'description': request.form.get('description')
        }
        
        if not all(data.values()):
            return jsonify({"error": "Missing required fields"}), 400

        photos = {
            'photo1': save_file('photo1'),
            'photo2': save_file('photo2'),
            'photo3': save_file('photo3'),
            'photo4': save_file('photo4'),
            'photo5': save_file('photo5')
        }

        cursor = db.cursor()
        sql = """
            INSERT INTO vehicules
            (user_id, marque, modele, prix, kilometrage, energie, type,description, photo1, photo2, photo3, photo4, photo5)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (*data.values(), *photos.values())
        cursor.execute(sql, values)
        db.commit()

        return jsonify({"message": "Vehicle added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_vehicule(id):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.*, v.description, u.nom as vendeur_nom, u.prenom as vendeur_prenom
            FROM vehicules v 
            JOIN users u ON v.user_id = u.id 
            WHERE v.id = %s
        """, (id,))
        vehicule = cursor.fetchone()
        
        if vehicule is None:
            return jsonify({"error": "Vehicle not found"}), 404
            
        return jsonify(vehicule)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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

    try:
        # Création du dossier devis s'il n'existe pas
        devis_path = os.path.join(app.config['UPLOAD_FOLDER'], 'devis')
        if not os.path.exists(devis_path):
            os.makedirs(devis_path)

        # Génération d'un nom de fichier unique
        filename = f"devis_{vehicule_id}_{session['user_id']}_{int(time.time())}.pdf"
        file_path = os.path.join(devis_path, filename)

        # Sauvegarde du fichier PDF
        with open(file_path, 'wb') as f:
            f.write(pdf_data)

        # Enregistrement dans la base de données
        cursor = db.cursor()
        sql = "INSERT INTO devis_pdf (user_id, vehicule_id, pdf_path) VALUES (%s, %s, %s)"
        cursor.execute(sql, (session['user_id'], vehicule_id, os.path.join('uploads/devis', filename)))
        db.commit()

        return jsonify({
            "message": "Devis enregistré avec succès",
            "pdf_path": os.path.join('uploads/devis', filename)
        }), 201

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
    
