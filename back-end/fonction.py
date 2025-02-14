from flask import Flask, render_template, request, redirect, session,jsonify
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_cors import CORS  # ✅ Importation de Flask-CORS


app = Flask(__name__)
CORS(app, supports_credentials=True)   # Active CORS pour toutes les routes
app.secret_key = 'buyandride'  # Clé secrète pour sécuriser les sessions
bcrypt = Bcrypt(app)

# Connexion à MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  
)

cursor = db.cursor()

# Création de la base de données et de la table si elles n'existent pas déjà
cursor.execute("CREATE DATABASE IF NOT EXISTS pythonlogin")
cursor.execute("USE pythonlogin")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nom VARCHAR(100),
        prenom VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255)
    )
""")
db.commit()

def register():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

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

