
from flask import Flask, request, jsonify, session, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'buyandride')  
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

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('PG_HOST', 'hetic.cd5ufp6fsve3.us-east-1.rds.amazonaws.com'),
        port=os.getenv('PG_PORT', '5432'),
        database=os.getenv('PG_DB', 'groupe4'),
        user=os.getenv('PG_USER', 'postgres'),
        password=os.getenv('PG_PASSWORD', 'LeContinent!')
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
        conn.commit()

        return jsonify({"message": "Vehicle created successfully", "id": cursor.lastrowid}), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()

# Implementer d'autres fonctions de manière similaire
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
