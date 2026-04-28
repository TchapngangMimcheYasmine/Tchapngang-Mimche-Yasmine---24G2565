from flask import Blueprint, request, jsonify
from models.db import get_db
from flask_jwt_extended import create_access_token
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/inscription', methods=['POST'])
def inscription():
    data = request.get_json()
    nom = data.get('nom')
    email = data.get('email')
    mot_de_passe = data.get('mot_de_passe')

    conn = get_db()
    cur = conn.cursor()

    cur.execute('SELECT * FROM users WHERE email = %s', (email,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({'message': 'Email déjà utilisé'}), 400

    hashed = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
    cur.execute('INSERT INTO users (nom, email, mot_de_passe) VALUES (%s, %s, %s)', (nom, email, hashed.decode('utf-8')))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Compte créé avec succès !'}), 201

@auth_bp.route('/connexion', methods=['POST'])
def connexion():
    data = request.get_json()
    email = data.get('email')
    mot_de_passe = data.get('mot_de_passe')

    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({'message': 'Email ou mot de passe incorrect'}), 400

    if not bcrypt.checkpw(mot_de_passe.encode('utf-8'), user[3].encode('utf-8')):
        return jsonify({'message': 'Email ou mot de passe incorrect'}), 400

    token = create_access_token(identity=str(user[0]))
    return jsonify({'token': token, 'user': {'id': user[0], 'nom': user[1], 'email': user[2]}})