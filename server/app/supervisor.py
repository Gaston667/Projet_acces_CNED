from flask import Blueprint, request
from datetime import timedelta, datetime, timezone
from flask import render_template, request, redirect, url_for, session
from database import DatabaseManager
from tools import generate_code, gerer_casse, generate_matricule, generate_password
import time
# from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import os
# from pyppeteer import launch

supervisor_blueprint = Blueprint('supervisor', __name__)
db_manager = DatabaseManager()

SESSION_TIMEOUT = 10 * 60


# Fonction de vérification de la session
@supervisor_blueprint.before_request
def verifier_session():
    if 'last_activity' in session:
        # Vérifie si la session a expiré
        if datetime.now(timezone.utc) - session['last_activity'] > timedelta(seconds=SESSION_TIMEOUT):
            # Déconnecte l'utilisateur si la session a expiré
            session.clear()
            return redirect(url_for('auth.loginun'))
    # Met à jour le timestamp de la dernière activité à chaque requête
    session['last_activity'] = datetime.now(timezone.utc)

# Page de supervision
@supervisor_blueprint.route('/supervision')
def supervision():
    print(session)
    if 'user' not in session:
        session.clear()
        return redirect(url_for('auth.loginun')) 
    
    else:
        # Le reste de votre code pour la page de supervision
        return render_template('supervisor_dashboard.html')  
        


                
# Page de gestion des codes
@supervisor_blueprint.route('/generate_code', methods=['GET', 'POST'])
def gestion_code():
    # Vérifier si l'utilisateur est connecté
    if 'user' not in session:
        return redirect(url_for('auth.login'))  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
    
    else:
        if request.method == 'POST': 
            code = generate_code()
            generated_at = datetime.now()
            expiration_date = generated_at + timedelta(seconds=60)  # 30 secondes de validité
            with db_manager:
                # Ajouter le code généré dans la base de données
                db_manager.add_generated_code(generated_code=code, generated_at=generated_at, expiration_date=expiration_date)
            return render_template('generate_unique_number.html', code=code)
        else:
            return render_template('generate_unique_number.html')

    



# Ajouter un nouvel eleve
@supervisor_blueprint.route('/supervision/ajouter_eleve', methods=['GET', 'POST'])
def ajout_eleve():
    success = False
    if 'user' not in session:
        return redirect(url_for('auth.loginun')) 

    elif request.method == 'POST':
        # matricule = request.form.get('Matricule')
        # mot_de_passe = request.form.get('password')
        mot_de_passe = generate_password()
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        classe = request.form.get('classe')
        identifiant_CNED = request.form.get('identifiant_CNED')  
        mot_de_passe_CNED = request.form.get('motdepassecned')
        
        # Gérer la casse des noms et prénoms
        nom = gerer_casse(nom, 'premiere_lettre')
        prenom = gerer_casse(prenom, 'premiere_lettre')
                
        while True:
            matricule = generate_matricule()
            with db_manager:
                existing_student = db_manager.get_student_by_matricule(matricule=matricule)
            if not existing_student:
                break  # Sortir de la boucle si le matricule est unique
        
        
        # Ajouter l'élève à la liste
        with db_manager:
            # Ajouter
            db_manager.add_student(matricule, mot_de_passe, identifiant_CNED, mot_de_passe_CNED, nom, prenom, classe) 
        success='Bravo eleve ajouter avec succes'
        return render_template('ajout.html', success=success)
    else:
        return render_template('ajout.html')  # Afficher le formulaire d'ajout d'élève

# Fonction pour rechercher un eleve
@supervisor_blueprint.route('/supervision/rechercher_eleve', methods=['GET', 'POST'])
def recherche_eleve():
    if 'user' not in session:
        return redirect(url_for('auth.loginun')) 
     
    if request.method == 'POST':
        donne = request.form.get('search')
        donne = gerer_casse(donne, 'premiere_lettre')
        # Vérifier si le texte entré ressemble à un matricule (commence par 2 lettres suivies de 2 chiffres)
        with db_manager:
            list_eleves = db_manager.get_student_by_nom(donne) 
        print(list_eleves)
    return render_template('ajout.html', list_eleves=list_eleves)

# Fonction pour afficher les informations d'un eleve
@supervisor_blueprint.route('/info_eleve/<matricule>')
def info_eleve(matricule):
    if 'user' not in session:
        return redirect(url_for('auth.loginun')) 
    
    # Utilisez la méthode get_student_by_matricule pour récupérer les informations de l'élève
    with db_manager:
        eleve = db_manager.get_student_by_matricule(matricule)
    
    # Vérifiez si l'élève existe
    if eleve:
        # Affichez les informations de l'élève dans une page HTML
        return render_template('info_eleve.html', eleve=eleve)
    else:
        # Si l'élève n'est pas trouvé, affichez un message d'erreur
        return "Aucun élève trouvé avec ce matricule."

# Fonction pour suprimer un eleve
@supervisor_blueprint.route('/suppression_eleve', methods=['POST'])
def suppression_eleve():
    if 'user' not in session:
        return redirect(url_for('auth.loginun')) 
     
    matricule = request.form.get('matricule')
    # Supprimer l'élève avec le matricule donné
    with db_manager:
        db_manager.delete_student(matricule)
    return redirect(url_for('routes.ajout_eleve'))

# Affichage des eleves
@supervisor_blueprint.route("/supervision/bdd_eleves")
def affichage_des_eleve():
    if 'user' not in session:
        return redirect(url_for('auth.loginun'))
    
    try:
        # Récupérer tous les élèves en utilisant la méthode get_all_students
        with db_manager:
            students = db_manager.get_all_students()
            
        
        if students:
            # Si des élèves sont récupérés, les passer à la page HTML
            return render_template('bdd_eleves.html', students=students)
        else:
            # Si aucun élève n'est récupéré, afficher un message d'erreur
            return "Aucun élève trouvé dans la base de données."
    except Exception as e:
        # Gérer les exceptions
        print("Erreur lors de l'affichage des élèves:", e)
        return "Une erreur s'est produite lors de l'affichage des élèves."


