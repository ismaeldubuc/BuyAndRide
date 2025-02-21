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
import json

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
    "origins": "http://localhost:5173",
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
    "supports_credentials": True
}})

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='hetic.cd5ufp6fsve3.us-east-1.rds.amazonaws.com',
            port='5432',
            database='groupe4',
            user='postgres',
            password='LeContinent!'
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise

def execute_query(query, params=None, fetch=True):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            conn.commit()
            return result
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def create_vehicle():
    try:
        data = request.json
        query = """
            INSERT INTO vehicules (marque, modele, prix, km, energie, photo1, photo2, photo3, photo4, photo5, type, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (data['marque'], data['modele'], data['prix'], data['km'], data['energie'],
                 data.get('photo1'), data.get('photo2'), data.get('photo3'), 
                 data.get('photo4'), data.get('photo5'),
                 data['type'], data['description'])
        execute_query(query, params, fetch=False)
        return jsonify({"message": "Vehicle created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_vehicle(id):
    try:
        data = request.json
        query = """
            UPDATE vehicules 
            SET marque = %s, modele = %s, prix = %s, km = %s, 
                energie = %s, photo1 = %s, photo2 = %s,
                photo3 = %s, photo4 = %s, photo5 = %s, type = %s, description = %s
            WHERE id = %s
        """
        params = (data['marque'], data['modele'], data['prix'], data['km'],
                 data['energie'], data['photo1'], data['photo2'],
                 data['photo3'], data['photo4'], data['photo5'],
                 data['type'], data['description'], id)
        rows_affected = execute_query(query, params, fetch=False)
        if rows_affected == 0:
            return jsonify({"error": "Vehicle not found"}), 404
        return jsonify({"message": "Vehicle updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_vehicle(id):
    try:
        query = "DELETE FROM vehicules WHERE id = %s"
        rows_affected = execute_query(query, (id,), fetch=False)
        if rows_affected == 0:
            return jsonify({"error": "Vehicle not found"}), 404
        return jsonify({"message": "Vehicle deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_vehicle():
    try:
        query = "SELECT * FROM vehicules"
        vehicles = execute_query(query)
        return jsonify(vehicles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_vehicle_by_id(id):
    try:
        query = """
            SELECT v.*, u.nom as vendeur_nom, u.prenom as vendeur_prenom 
            FROM vehicules v 
            JOIN users u ON v.user_id = u.id 
            WHERE v.id = %s
        """
        vehicle = execute_query(query, (id,))
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
            
        vehicle_dict = dict(vehicle[0])
        for i in range(1, 6):
            photo_key = f'photo{i}'
            if vehicle_dict.get(photo_key):
                vehicle_dict[photo_key] = os.path.join('uploads', os.path.basename(vehicle_dict[photo_key]))
                
        return jsonify(vehicle_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def register():
    if request.method == 'POST':
        try:
            data = request.json
            password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            query = "INSERT INTO users (nom, prenom, email, mdp) VALUES (%s, %s, %s, %s)"
            params = (data['nom'], data['prenom'], data['email'], password_hash)
            execute_query(query, params, fetch=False)
            return jsonify({"message": "Inscription réussie"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

def login():
    try:
        data = request.get_json()
        query = "SELECT * FROM users WHERE email = %s"
        users = execute_query(query, (data['email'],))
        if users and bcrypt.check_password_hash(users[0]['mdp'], data['password']):
            session['user_id'] = users[0]['id']
            return jsonify({"message": "Connexion réussie"}), 200
        return jsonify({"message": "Identifiants incorrects"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def profile():
    if 'user_id' not in session:
        return jsonify({"error": "Utilisateur non authentifié"}), 401

    try:
        query = "SELECT nom, prenom, email FROM users WHERE id = %s"
        users = execute_query(query, (session['user_id'],))
        if not users:
            return jsonify({"error": "Utilisateur non trouvé"}), 404
        return jsonify(dict(users[0]))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def modif_profil():
    if 'user_id' not in session:
        return jsonify({"error": "Utilisateur non authentifié"}), 401

    try:
        if request.method == 'POST':
            if 'changer_mdp' in request.form:
                new_password = request.form.get('new_password')
                confirm_password = request.form.get('confirm_password')

                if new_password != confirm_password:
                    return jsonify({"error": "Les mots de passe ne correspondent pas"}), 400

                new_password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
                query = "UPDATE users SET mdp = %s WHERE id = %s"
                execute_query(query, (new_password_hash, session['user_id']), fetch=False)
                return jsonify({"message": "Mot de passe mis à jour avec succès"}), 200
            else:
                query = "UPDATE users SET nom=%s, prenom=%s, email=%s WHERE id=%s"
                params = (request.form.get('nom'), request.form.get('prenom'), 
                         request.form.get('email'), session['user_id'])
                execute_query(query, params, fetch=False)
                return jsonify({"message": "Profil mis à jour avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Déconnexion réussie"}), 200

def list_vehicules():
    if 'user_id' not in session:
        return jsonify({"error": "Authentication required"}), 401
    try:
        query = "SELECT * FROM vehicules WHERE user_id = %s"
        vehicules = execute_query(query, (session['user_id'],))
        return jsonify(vehicules)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def add_vehicule():
    if 'user_id' not in session:
        return jsonify({"error": "Authentication required"}), 401
    try:
        data = request.json
        query = """
            INSERT INTO vehicules (user_id, marque, modele, prix, kilometrage, energie, type, description, 
                                 photo1, photo2, photo3, photo4, photo5) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (session['user_id'], data['marque'], data['modele'], data['prix'], 
                 data['kilometrage'], data['energie'], data['type'], data['description'],
                 data['photo1'], data['photo2'], data['photo3'], data['photo4'], data['photo5'])
        execute_query(query, params, fetch=False)
        return jsonify({"message": "Vehicle added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_vehicule(id):
    try:
        query = """
            SELECT v.*, u.nom as vendeur_nom, u.prenom as vendeur_prenom 
            FROM vehicules v 
            JOIN users u ON v.user_id = u.id 
            WHERE v.id = %s
        """
        vehicule = execute_query(query, (id,))
        if not vehicule:
            return jsonify({"error": "Vehicle not found"}), 404
        return jsonify(dict(vehicule[0]))
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
        devis_path = os.path.join(app.config['UPLOAD_FOLDER'], 'devis')
        if not os.path.exists(devis_path):
            os.makedirs(devis_path)
        filename = f"devis_{vehicule_id}_{session['user_id']}_{int(time.time())}.pdf"
        file_path = os.path.join(devis_path, filename)
        with open(file_path, 'wb') as f:
            f.write(pdf_data)
        
        query = "INSERT INTO devis_pdf (user_id, vehicule_id, pdf_path) VALUES (%s, %s, %s)"
        params = (session['user_id'], vehicule_id, os.path.join('uploads/devis', filename))
        execute_query(query, params, fetch=False)
        return jsonify({"message": "Devis enregistré avec succès", 
                       "pdf_path": os.path.join('uploads/devis', filename)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def filter_vehicules():
    try:
        conditions = []
        params = []
        
        if request.args.get('marque'):
            conditions.append("marque = %s")
            params.append(request.args.get('marque'))
        
        if request.args.get('modele'):
            conditions.append("modele = %s")
            params.append(request.args.get('modele'))
            
        if request.args.get('prix'):
            conditions.append("prix <= %s")
            params.append(request.args.get('prix'))
            
        if request.args.get('kilometrage'):
            conditions.append("km <= %s")
            params.append(request.args.get('kilometrage'))
            
        if request.args.get('energie'):
            conditions.append("energie = %s")
            params.append(request.args.get('energie'))
            
        if request.args.get('type'):
            conditions.append("type = %s")
            params.append(request.args.get('type'))
            
        query = "SELECT * FROM vehicules"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        vehicules = execute_query(query, tuple(params))
        response = {"vehicules": vehicules}
        if request.args.get('type'):
            response["type"] = request.args.get('type')
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_type_vehicule(id):
    try:
        data = request.json
        query = "UPDATE vehicules SET type = %s WHERE id = %s"
        params = (data['type'], id)
        execute_query(query, params, fetch=False)
        return jsonify({"message": "Etat du véhicule mis à jour avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_achat_vehicule():
    try:
        query = "SELECT * FROM vehicules WHERE type = 'true'"
        vehicules = execute_query(query)
        return jsonify(vehicules), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_louer_vehicule():
    try:
        query = "SELECT * FROM vehicules WHERE type = 'false'"
        vehicules = execute_query(query)
        return jsonify(vehicules), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_marques():
    try:
        query = "SELECT DISTINCT marque FROM vehicules ORDER BY marque"
        marques = [row[0] for row in execute_query(query)]
        return jsonify(marques)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_modeles(marque):
    try:
        query = "SELECT DISTINCT modele FROM vehicules WHERE marque = %s ORDER BY modele"
        modeles = [row[0] for row in execute_query(query, (marque,))]
        return jsonify(modeles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def filter_vehicles():
    try:
        conditions = []
        params = []
        
        if request.args.get('marque'):
            conditions.append("v.marque = %s")
            params.append(request.args.get('marque'))
            
        if request.args.get('modele'):
            conditions.append("v.modele = %s")
            params.append(request.args.get('modele'))
            
        if request.args.get('energie'):
            conditions.append("v.energie = %s")
            params.append(request.args.get('energie'))
            
        if request.args.get('prix'):
            conditions.append("v.prix <= %s")
            params.append(float(request.args.get('prix')))
            
        if request.args.get('kilometrage'):
            conditions.append("v.kilometrage <= %s")
            params.append(int(request.args.get('kilometrage')))
            
        query = """
            SELECT v.*, u.nom as vendeur_nom, u.prenom as vendeur_prenom
            FROM vehicules v 
            JOIN users u ON v.user_id = u.id
        """
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        vehicles = execute_query(query, tuple(params))
        
        vehicles_list = []
        for vehicle in vehicles:
            vehicle_dict = dict(vehicle)
            for i in range(1, 6):
                photo_key = f'photo{i}'
                if vehicle_dict.get(photo_key):
                    vehicle_dict[photo_key] = os.path.join('uploads', os.path.basename(vehicle_dict[photo_key]))
            vehicles_list.append(vehicle_dict)
        
        return jsonify(vehicles_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
