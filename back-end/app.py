from flask import Flask, render_template, request, redirect, session,jsonify
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_cors import CORS  # ✅ Importation de Flask-CORS
from fonction import register, login, profile, logout
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

@app.route('/')
def home():
      return render_template('login.html')

@app.route('/register', methods=['POST'])
def register_route():
      return register()

@app.route('/login', methods=['POST'])
def login_route():
      return login()

@app.route('/profile', methods=['GET', 'POST'])
def profile_route():
      return profile()

@app.route('/logout', methods=['POST'])
def logout_route():
      return logout()

if __name__ == '__main__':
      app.run(debug=True)
