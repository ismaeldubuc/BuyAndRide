
from flask import Flask, render_template, request, redirect, session,jsonify
import mysql.connector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
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

@app.route('/register', methods=['GET', 'POST'])
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
            return redirect('/')
        except mysql.connector.Error as err:
            return f"Erreur : {err}"
    return render_template('register.html')


@app.route('/login',  methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect('/profile')
        return "Identifiants incorrects"
   return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect('/')
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()

    if request.method == 'POST':
        if 'changer_mdp' in request.form:
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            if new_password == confirm_password:
                new_password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
                cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password_hash, session['user_id']))
                db.commit()
                return "Mot de passe mis à jour avec succès"
            else:
                return "Les mots de passe ne correspondent pas"
        else:
            nom = request.form['nom']
            prenom = request.form['prenom']
            email = request.form['email']

            cursor.execute("UPDATE users SET nom=%s, prenom=%s, email=%s WHERE id=%s", (nom, prenom, email, session['user_id']))
            db.commit()
            return redirect('/profile')

    return render_template('profile.html', user=user)
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')



# Route pour obtenir les photos d'un véhicule

# @app.route('/vehicules/<int:id>/photos', methods=['GET'])
# def get_vehicle_photos(id):
#     try:
#         mycursor = db.cursor()
#         sql = "SELECT photo_url FROM photos_vehicules WHERE vehicule_id = %s"
#         val = (id,)
#         mycursor.execute(sql, val)
#         myresult = mycursor.fetchall()

#         if not myresult:
#             return jsonify({"message": "Aucune photo trouvée pour ce véhicule"}), 404

#         # Extraire les URLs des photos
#         photo_urls = [row[0] for row in myresult] # Récupère l'URL à l'index 0 de chaque ligne
#         return jsonify(photo_urls), 200

#     except Exception as e:
#         print(f"Erreur : {e}")
#         return jsonify({"message": "Erreur serveur"}), 500



if __name__ == '__main__':
    app.run(debug=True)
