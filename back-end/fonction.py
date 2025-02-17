from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import mysql.connector
import os


app = Flask(__name__)
app.secret_key = 'buyandride'  


def get_db_connection():
    mysql_conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DB')
    )
    return mysql_conn

def create_vehicle():
    data = request.json
    mysql_conn = get_db_connection()
    cursor = mysql_conn.cursor()

    try:
        query = """
            INSERT INTO vehicules (marque, modele, prix, km, energie, photo1, photo2, photo3, photo4, photo5, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            data.get('description')
        )

        # Exécution de la requête
        cursor.execute(query, values)
        mysql_conn.commit()

        return jsonify({"message": "Vehicle created successfully", "id": cursor.lastrowid}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        mysql_conn.close()

def update_vehicle():
    data = request.json
    vehicle_id = data.get('id')
    
    mysql_conn = get_db_connection()
    cursor = mysql_conn.cursor()

    try:
        query = """
            UPDATE vehicules 
            SET marque = %s, modele = %s, prix = %s, km = %s, 
                energie = %s, type = %s, photo1 = %s, photo2 = %s,
                photo3 = %s, photo4 = %s, photo5 = %s, description = %s
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
            data.get('description'),
            vehicle_id
        )

        cursor.execute(query, values)
        mysql_conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Vehicle not found"}), 404

        return jsonify({"message": "Vehicle updated successfully"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        mysql_conn.close()

def delete_vehicle():
    data = request.json
    vehicle_id = data.get('id')

    mysql_conn = get_db_connection()
    cursor = mysql_conn.cursor()

    try:
        query = "DELETE FROM vehicules WHERE id = %s"
        cursor.execute(query, (vehicle_id,))
        mysql_conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Vehicle not found"}), 404

        return jsonify({"message": "Vehicle deleted successfully"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        mysql_conn.close()

def get_vehicle():
    mysql_conn = get_db_connection()
    cursor = mysql_conn.cursor(dictionary=True)

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
        mysql_conn.close()

