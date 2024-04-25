from flask import Blueprint, request, jsonify, session
from datetime import timedelta, datetime, timezone
from database import DatabaseManager
from tools import generate_code
import time

SESSION_TIMEOUT = 30

eleves_blueprint = Blueprint('eleves', __name__)
db_manager = DatabaseManager()

# Fonction de vérification de la session
@eleves_blueprint.before_request
def verifier_session():
    if 'last_activity' in session:
        # Vérifie si la session a expiré
        if datetime.now(timezone.utc) - session['last_activity'] > timedelta(seconds=SESSION_TIMEOUT):
            # Déconnecte l'utilisateur si la session a expiré
            session.clear()
            return jsonify({'message': 'Session expirée'}), 401
    # Met à jour le timestamp de la dernière activité à chaque requête
    session['last_activity'] = datetime.now(timezone.utc)


# Route pour la connexion avec un code
@eleves_blueprint.route('/verifcode', methods=['POST'])
def verifcode():
    if 'user' not in session:
        session.clear()
        return jsonify({'message': 'Utilisateur non connecté'}), 401
    
    
    data = request.get_json()
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
            return jsonify({'message': 'Connexion réussie'})
        else:
            return jsonify({'message': 'Code invalide. Veuillez réessayer.'}), 400
    else:
        return jsonify({'message': 'Code invalide. Veuillez réessayer.'}), 400







# @routes_blueprint.route('/login-verification', methods=['POST', 'GET'])
# def loginverifation():
#     if 'user' not in session:
#         return redirect(url_for('auth.loginun'))  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
#     elif session['user']['role'] == 'user':
#         if request.method == 'POST':
#             code = request.form.get('code')
            
#             with db_manager:
#                 code_info = db_manager.get_generated_code(code)
                
                
#             current_time = datetime.now()
#             if code_info:
#                 expiration_date = datetime.strptime(code_info[0]['expiration_date'], '%Y-%m-%d %H:%M:%S.%f')
#                 if current_time < expiration_date:
#                     # Code pour récupérer les informations de l'utilisateur et remplir les champs du formulaire CNED
#                     identifiant_cned = session['user']['identifiant_CNED']
#                     mot_de_passe_cned = session['user']['mot_de_passe_CNED']
                                   
#                     # #Creer une variable qui pour declancher le navigateur
#                     # #diver_path est le chemin vers le chromedriver
#                     # drver_path = "chromedriver.exe"
#                     # driver = webdriver.Chrome()
                    
#                     # # url vers la page d'acceuille du CNED
#                     # # url = "https://www.cned360.fr/uPortal/p/home"
#                     # # url vers la page de connexion du CNED
#                     # url = "https://sts.cned.fr/adfs/ls/?wtrealm=https%3A%2F%2Fespaceinscrit.cned.fr&wctx=WsFedOwinState%3D1kJs2CMiqSTWgXUULhuPNagdvV-hz-c0o_YiPEvrc0TVYGnFCjzdXTjK607t2ugcX3LlaTG5zwr1FJY85ayG05QkW5XnQqmD5haiXJCmkIXf7L6jrYh0Hd1zJO5CVObkEVFqF0xYunS-fZboGWE2SyIv_373XDJ2P4CAoqKdSx4&wa=wsignin1.0"
                
#                     # # Ouvrir la page de connexion CNED
#                     # driver.get(url)  
#                     # # time.sleep(4)
                    
#                     # # driver.close()
                    
                    
                    

#                     # # Remplir les champs du formulaire de connexion CNED avec les informations de l'utilisateur
#                     # identifiant_input = driver.find_element('name', 'UserName')
#                     # identifiant_input.send_keys(identifiant_cned)
#                     # mot_de_passe_input = driver.find_element('name','Password')
#                     # mot_de_passe_input.send_keys(mot_de_passe_cned) 
                        
#                     # # Soumettre le formulaire de connexion CNED
#                     # submit_button = driver.find_element('id','submitButton')
#                     # submit_button.click()
                        
#                     # time.sleep(5)
                    
#                     # # Récupérer le processus WebDriver
#                     # webdriver_process = driver.service.process
#                     # # Obtenez le pid du processus du pilote WebDriver
#                     # webdriver_process_name = webdriver_process.pid
#                     # # Tuer le processus WebDriver
#                     # os.system("taskkill /f /pid {}".format(webdriver_process_name))
                    

#                     # return redirect(url_for('auth.logout'))
#                     return render_template('login.html')
#                 else:
#                     return render_template('login.html', message="Code invalide. Veuillez reessayer avec un code valide.")
#             else:
#                 return render_template('login.html', message="Code invalide. Veuillez reessayer.")
#     else:
#         session.clear()
#         return render_template('usurpation.html')

