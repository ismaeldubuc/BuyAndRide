import time
from flask import Flask, request, jsonify, session , send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt_identity
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv
from flask_cors import CORS
import time
import json
from app import get_db_connection

load_dotenv()

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
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        query = """
            SELECT v.*, u.nom as vendeur_nom, u.prenom as vendeur_prenom 
            FROM vehicules v 
            JOIN users u ON v.user_id = u.id 
            WHERE v.id = %s
        """
        cursor.execute(query, (id,))
        vehicle = cursor.fetchone()
        if vehicle is None:
            return jsonify({"error": "Vehicle not found"}), 404
            
        vehicle_dict = dict(vehicle)
        # Transformer les chemins d'images
        for i in range(1, 6):
            photo_key = f'photo{i}'
            if vehicle_dict.get(photo_key):
                vehicle_dict[photo_key] = os.path.join('uploads', os.path.basename(vehicle_dict[photo_key]))
                
        return jsonify(vehicle_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
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
            session.clear()
            session['user_id'] = user['id']
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
    if 'user_id' in session:
        return jsonify({"isAuthenticated": True, "user_id": session['user_id']}), 200
    return jsonify({"isAuthenticated": False}), 401

def profile():
    logging.debug("Checking if user is authenticated")
    if 'user_id' not in session:
        logging.debug("No user_id in session")
        return jsonify({"error": "Utilisateur non authentifié"}), 401

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)

    try:
        logging.debug(f"Fetching user data for user_id: {user_id}")
        cursor.execute("SELECT nom, prenom, email FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            logging.debug("User not found in database")
            return jsonify({"error": "Utilisateur non trouvé"}), 404

        logging.debug("User data retrieved successfully")
        user_json = json.dumps(user, indent=4)
        logging.debug("JSON data to be returned: " + user_json)
        return jsonify(user)
    except Exception as e:
        logging.error(f"Error retrieving user data: {str(e)}")
        return jsonify({"error": "Erreur lors de la récupération des données : " + str(e)}), 500
    finally:
        cursor.close()
        conn.close()

def modif_profil():
    logging.debug("Checking if user is authenticated")
    if 'user_id' not in session:
        logging.debug("No user_id in session")
        return jsonify({"error": "Utilisateur non authentifié"}), 401

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)

    try:
        if request.method == 'POST':
            if 'changer_mdp' in request.form:
                # Changement de mot de passe
                new_password = request.form.get('new_password')
                confirm_password = request.form.get('confirm_password')

                if new_password != confirm_password:
                    logging.debug("Passwords do not match")
                    return jsonify({"error": "Les mots de passe ne correspondent pas"}), 400

                new_password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
                cursor.execute("UPDATE users SET mdp = %s WHERE id = %s", (new_password_hash, user_id))
                conn.commit()
                logging.debug("Password updated successfully")
                return jsonify({"message": "Mot de passe mis à jour avec succès"}), 200

            else:
                # Modification des infos du profil
                nom = request.form.get('nom')
                prenom = request.form.get('prenom')
                email = request.form.get('email')

                cursor.execute("UPDATE users SET nom=%s, prenom=%s, email=%s WHERE id=%s",
                               (nom, prenom, email, user_id))
                conn.commit()
                logging.debug("Profile updated successfully")
                return jsonify({"message": "Profil mis à jour avec succès"}), 200

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Erreur lors de la mise à jour des données : " + str(e)}), 500
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
        return jsonify({"error": str(e)}), 500

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
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute("SELECT DISTINCT marque FROM vehicules ORDER BY marque")
        marques = [row[0] for row in cursor.fetchall()]
        return jsonify(marques)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
    
def get_modeles(marque):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute("SELECT DISTINCT modele FROM vehicules WHERE marque = %s ORDER BY modele", (marque,))
        modeles = [row[0] for row in cursor.fetchall()]
        return jsonify(modeles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

def filter_vehicles():
    try:
        marque = request.args.get('marque')
        modele = request.args.get('modele')
        energie = request.args.get('energie')
        prix_max = request.args.get('prix')
        km_max = request.args.get('kilometrage')

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        query = """
            SELECT v.*, u.nom as vendeur_nom, u.prenom as vendeur_prenom
            FROM vehicules v 
            JOIN users u ON v.user_id = u.id 
            WHERE 1=1
        """
        params = []

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

        # Convertir les résultats en liste de dictionnaires
        vehicles_list = []
        for vehicle in vehicles:
            vehicle_dict = dict(vehicle)
            # Transformer les chemins d'images
            for i in range(1, 6):
                photo_key = f'photo{i}'
                if vehicle_dict.get(photo_key):
                    vehicle_dict[photo_key] = os.path.join('uploads', os.path.basename(vehicle_dict[photo_key]))
            vehicles_list.append(vehicle_dict)
        
        return jsonify(vehicles_list)

    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
