from flask import Blueprint
import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from database import DatabaseManager
from tools import generate_code
routes_blueprint = Blueprint('routes', __name__)
db_manager = DatabaseManager()

@routes_blueprint.route('/logincode', methods=['POST', 'GET'])
def logincode():
    # Vérifier si l'utilisateur est connecté
    if 'user' not in session:
        return redirect(url_for('auth.loginun'))  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
    return render_template('login.html')

@routes_blueprint.route('/generate_code', methods=['GET', 'POST'])
def gesgition_code():
    # Vérifier si l'utilisateur est connecté
    if 'user' not in session:
        return redirect(url_for('auth.loginun'))  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
    
    if request.method == 'POST':
        code = generate_code()
        generated_at = datetime.datetime.now()
        expiration_date = generated_at + datetime.timedelta(seconds=30)  # 30 secondes de validité
        with db_manager:
            # Ajouter le code généré dans la base de données
            db_manager.manage_generated_codes('add', generated_code=code, generated_by='supervisor', generated_at=generated_at, expiration_date=expiration_date)
            # ('add', generated_code=code, generated_by='supervisor', generated_at=generated_at, expiration_date=expiration_date)
            return render_template('generate_unique_number.html', code=generate_code())
    else:
        return render_template('generate_unique_number.html')

@routes_blueprint.route('/supervision')
def supervision():
    return render_template('supervisor_dashboard.html')




