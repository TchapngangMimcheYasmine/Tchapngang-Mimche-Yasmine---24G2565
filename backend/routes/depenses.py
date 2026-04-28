from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db import get_db

depenses_bp = Blueprint('depenses', __name__)

@depenses_bp.route('/', methods=['POST'])
@jwt_required()
def ajouter():
    user_id = get_jwt_identity()
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO depenses (user_id, montant, categorie, description, date) VALUES (%s, %s, %s, %s, %s)',
        (user_id, data['montant'], data['categorie'], data.get('description', ''), data['date'])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Dépense ajoutée !'}), 201

@depenses_bp.route('/', methods=['GET'])
@jwt_required()
def get_depenses():
    user_id = get_jwt_identity()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM depenses WHERE user_id = %s ORDER BY date DESC', (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    depenses = [{'id': r[0], 'user_id': r[1], 'montant': float(r[2]), 'categorie': r[3], 'description': r[4], 'date': str(r[5])} for r in rows]
    return jsonify(depenses)

@depenses_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def supprimer(id):
    user_id = get_jwt_identity()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM depenses WHERE id = %s AND user_id = %s', (id, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Dépense supprimée !'}), 200

@depenses_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def modifier(id):
    user_id = get_jwt_identity()
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'UPDATE depenses SET montant=%s, categorie=%s, description=%s, date=%s WHERE id=%s AND user_id=%s',
        (data['montant'], data['categorie'], data.get('description', ''), data['date'], id, user_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Dépense modifiée !'}), 200