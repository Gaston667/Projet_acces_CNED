from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from database import DatabaseManager
from werkzeug.security import check_password_hash
from tools import gerer_casse

auth_blueprint = Blueprint('auth', __name__)

# Initialisation de la base de données
db_manager = DatabaseManager()

# Autres routes d'authentification si nécessaire
@auth_blueprint.route('/', methods=['POST', 'GET'])
def loginun():
    if request.method == 'POST':  
        session.pop('user', None)    
        # Récupère les données du formulaire
        matricule = gerer_casse(request.form['matricule'], 'majuscules')
        password = request.form['password']
        
        # Vérifie si les champs matricule, password et role sont remplis
        if matricule and password :
            # Vérifier le role de l'utilisateur (direction ou enseignant ou eleve)
            
            # Utilisation du gestionnaire de contexte 'with' pour assurer une gestion appropriée de la connexion à la base de données
            with db_manager:
               # Récupère les informations de l'utilisateur (enseignant) à partir de la base de données
                enseignantliste = {'nom': 'SUPERVISOR', 'matricule': 'SP92', 'mot_de_passe': '1234'}
                # Vérifie si l'utilisateur a été trouvé dans la base de données
                if enseignantliste:
                    if enseignantliste['matricule'] == matricule and enseignantliste['mot_de_passe'] == password:
                        #BDD
                        session['user'] = {
                            'nom': enseignantliste['nom'],
                            'matricule': enseignantliste['matricule']
                        }   
                        
                        # Utilisateur authentifié, effectue la redirection vers le tableau de bord de la direction
                        return redirect(url_for('supervisor.supervision'))
                    else:
                        # Matricule ou mot de passe incorrect, affiche un message d'erreur
                        return render_template('loginun.html', message='Matricule ou mot de passe incorrect')
                else:
                    # Utilisateur non trouvé dans la base de données, affiche un message d'erreur
                    return render_template('loginun.html', message='Utilisateur non trouvé')
        else:
            # Champs manquants, affiche un message d'erreur
            return render_template('loginun.html', message='Champs manquants')
    # Si la méthode HTTP n'est pas POST, renvoyer le formulaire de connexion
    return render_template('loginun.html')
    
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'matricule' not in data or 'password' not in data:
        return jsonify({'error': 'Données manquantes'}), 400
    
    matricule = gerer_casse(data['matricule'], 'majuscules')
    password = data['password']
    


    with db_manager:
        eleve = db_manager.get_student_by_matricule(matricule=matricule)
        if eleve and eleve['mot_de_passe'] == password:
            session['user'] = {
                'matricule': eleve['matricule'],
                'identifiant_CNED': eleve['identifiant_CNED'],
                'mot_de_passe_CNED': eleve['mot_de_passe_CNED'],
                'nom': eleve['nom'],
                'prenom': eleve['prenom'],
                'classe': eleve['classe'],
            }
            return jsonify({'message': 'Connexion réussie', 'session_data': session}), 200
        else:
            return jsonify({'message': 'Identifiants incorrects'}), 401
        
# Ajouter cette méthode pour déconnecter l'utilisateur et supprimer la session
@auth_blueprint.route('/logout')
def logout():
    # Effacer les informations de session
    session.clear()
    # Rediriger l'utilisateur vers la page de connexion par exemple
    return render_template('logout.html')