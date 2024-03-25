from flask import Blueprint, render_template, request, redirect, url_for, session
from database import DatabaseManager
from werkzeug.security import check_password_hash
auth_blueprint = Blueprint('auth', __name__)

# Initialisation de la base de données
db_manager = DatabaseManager()

# Autres routes d'authentification si nécessaire
@auth_blueprint.route('/', methods=['POST', 'GET'])
def loginun():
    if request.method == 'POST':      
        # Récupère les données du formulaire
        matricule = request.form['matricule']
        password = request.form['password']
        role = request.form['role']
        # Vérifie si les champs matricule, password et role sont remplis
        if matricule and password and role != '':
            # Vérifier le role de l'utilisateur (direction ou enseignant ou eleve)
            if role == 'enseignant':
                # Utilisation du gestionnaire de contexte 'with' pour assurer une gestion appropriée de la connexion à la base de données
                with db_manager:
                   # Récupère les informations de l'utilisateur (enseignant) à partir de la base de données
                    enseignantliste = {'nom': 'Diallo', 'prenom': 'Algassimou', 'matricule': 'LOL', 'mot_de_passe': '1234'}
                    # Vérifie si l'utilisateur a été trouvé dans la base de données
                    if enseignantliste:
                        if enseignantliste['matricule'] == matricule and enseignantliste['mot_de_passe'] == password:
                            #BDD
                            session['user'] = {
                                'nom': enseignantliste['nom'],
                                'mastricule': enseignantliste['matricule'],
                                'prenom': enseignantliste['prenom']
                            }
                            # Utilisateur authentifié, effectue la redirection vers le tableau de bord de la direction
                            return redirect(url_for('routes.supervisor_dashbord'))
                        else:
                            # Matricule ou mot de passe incorrect, affiche un message d'erreur
                            return render_template('loginun.html', message='Matricule ou mot de passe incorrect')
                    else:
                        # Utilisateur non trouvé dans la base de données, affiche un message d'erreur
                        return render_template('loginun.html', message='Utilisateur non trouvé')
        
            # Vérifier le role de l'utilisateur (direction ou enseignant ou eleve)
            if role == 'eleve':
                # Utilisation du gestionnaire de contexte 'with' pour assurer une gestion appropriée de la connexion à la base de données
                with db_manager:
                    # Récupère les informations de l'utilisateur (enseignant) à partir de la base de données
                    eleveliste = db_manager.manage_students('get', matricule=matricule)
                    # Vérifie si l'utilisateur a été trouvé dans la base de données
                    if eleveliste:
                        eleve = eleveliste
                        # Vérifie le mot de passe hashé
                        if check_password_hash(eleve['mot_de_passe'], password) :
                            print(eleveliste)
                            #Session 
                            session['user'] = {
                                'mastricule': eleveliste['matricule'],
                                'nom': eleveliste['nom'],
                                'prenom': eleveliste['prenom']
                            }
                            # Utilisateur authentifié, effectue la redirection vers le tableau de bord de la direction
                            return redirect(url_for('routes.logincode'))
                        else:
                            # Mot de passe incorrect, affiche un message d'erreur
                            return render_template('loginun.html', message='Mot de passe incorrect')
                    else:
                        # Utilisateur non trouvé dans la base de données, affiche un message d'erreur
                        return render_template('loginun.html', message='Utilisateur non trouvé')  
                    
    # Si la méthode HTTP n'est pas POST, renvoyer le formulaire de connexion
    return render_template('loginun.html')
        

# Ajouter cette méthode pour déconnecter l'utilisateur et supprimer la session
@auth_blueprint.route('/logout')
def logout():
    # Effacer les informations de session
    session.clear()
    # Rediriger l'utilisateur vers la page de connexion par exemple
    return redirect(url_for('auth.loginun'))