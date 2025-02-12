from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Définir le dossier d'upload (assurez-vous qu'il existe)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Configuration de la connexion à la base de données
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pythonlogin"
)

def save_file(file_key):
    """
    Sauvegarde le fichier uploadé dans le dossier UPLOAD_FOLDER.
    Retourne le chemin relatif (par rapport au dossier 'static') à enregistrer en BDD.
    """
    file = request.files.get(file_key)
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        # Chemin absolu pour sauvegarder le fichier
        absolute_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(absolute_path)
        # On enregistre uniquement le chemin relatif (ex: "uploads/monfichier.jpg")
        relative_path = os.path.join('uploads', filename)
        return relative_path
    return None

# Route pour afficher tous les véhicules sur une page HTML
@app.route('/vehicules', methods=['GET'])
def list_vehicules():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vehicules")
        vehicules = cursor.fetchall()
        return render_template('annonce.html', vehicules=vehicules)
    except Exception as e:
        print("Erreur lors de la récupération des véhicules :", e)
        return "Erreur serveur", 500

# Route pour ajouter un nouveau véhicule dans la base de données
@app.route('/vehicules', methods=['POST'])
def add_vehicule():
    try:
        # Récupérer les champs texte
        marque         = request.form.get('marque')
        modele         = request.form.get('modele')
        prix           = request.form.get('prix')
        kilometrage    = request.form.get('kilometrage')
        energie        = request.form.get('energie')
        type_vehicule  = request.form.get('type')

        # Vérifier que les champs obligatoires sont fournis
        if not all([marque, modele, prix, kilometrage, energie, type_vehicule]):
            return "Tous les champs obligatoires ne sont pas fournis", 400

        # Sauvegarder les fichiers uploadés (s'ils existent)
        photo1 = save_file('photo1')
        photo2 = save_file('photo2')
        photo3 = save_file('photo3')
        photo4 = save_file('photo4')
        photo5 = save_file('photo5')

        cursor = db.cursor()
        sql = """
            INSERT INTO vehicules 
            (marque, modele, prix, kilometrage, energie, type, photo1, photo2, photo3, photo4, photo5)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (marque, modele, prix, kilometrage, energie, type_vehicule, photo1, photo2, photo3, photo4, photo5)
        cursor.execute(sql, values)
        db.commit()
        
        return redirect(url_for('list_vehicules'))
    except Exception as e:
        print("Erreur lors de l'insertion du véhicule :", e)
        return "Erreur serveur", 500

if __name__ == '__main__':
    app.run(debug=True)
