from flask import Blueprint, request, jsonify, session
from datetime import timedelta, datetime, timezone
from database import DatabaseManager
from tools import generate_code
import time

SESSION_TIMEOUT = 5

eleves_blueprint = Blueprint('eleves', __name__)
db_manager = DatabaseManager()

# Fonction de vérification de la session
@eleves_blueprint.before_request
def verifier_session():
    data_session_cookie = request.get_json().get('session_data')
    print(f"Before _ request :{session}")
    session['user'] = data_session_cookie['user']


# Route pour la connexion avec un code
@eleves_blueprint.route('/verifcode', methods=['POST'])
def verifcode():
    data = request.get_json()
    if 'user' not in session:
        session.clear()
        return jsonify({'message': 'Utilisateur non connecté'}), 401
    
    
    if not data or 'code' not in data:
        return jsonify({'message': 'Code manquant'}), 400

    code = data['code']

    # Récupérer les informations sur le code depuis la base de données
    with db_manager:
        code_info = db_manager.get_generated_code(code)

    current_time = datetime.now()
    # Vérifier si le code existe dans la base de données et s'il est toujours valide
    if code_info:
        expiration_date = datetime.strptime(code_info[0]['expiration_date'], '%Y-%m-%d %H:%M:%S.%f')
        if current_time < expiration_date:
            # Si le code est valide, enregistrer le code dans la session de l'utilisateur
            session['user']['code'] = code_info[0]
            return jsonify({'message': 'Connexion réussie'}), 200
        else:
            return jsonify({'message': 'Code invalide. Veuillez réessayer.'}), 400
    else:
        return jsonify({'message': 'Code invalide. Veuillez réessayer.'}), 400






