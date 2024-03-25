import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class DatabaseManager:
    print("Connexion avec la base de données...")
    def __init__(self):
        self.db_name = './database/database.db'
        self.conn = None
        self.cursor = None  # Initialisez le curseur ici

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()  # Initialisez le curseur ici
        print("Connexion avec la base de données reussie.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()


    # Les autres méthodes de la classe DatabaseManager restent inchangées

    def create_tables(self):
        # Créer la table des élèves
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS eleves (
                                matricule TEXT NOT NULL PRIMARY KEY,
                                mot_de_passe TEXT NOT NULL,
                                nom TEXT NOT NULL,
                                prenom TEXT NOT NULL,
                                classe TEXT NOT NULL
                        )'''
        )
    
        # # Créer la table des enseignants
        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS enseignants (
        #                         matricule TEXT NOT NULL PRIMARY KEY,
        #                         mot_de_passe TEXT NOT NULL,
        #                         nom TEXT NOT NULL,
        #                         prenom TEXT NOT NULL
        #                 )'''
        # )
        
        
        # Créer la table des ID_CNED
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS id_cned (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                eleve_matricule TEXT NOT NULL,
                                identifiant_CNED TEXT NOT NULL,
                                mot_de_passe_CNED TEXT NOT NULL,
                                FOREIGN KEY(eleve_matricule) REFERENCES eleves(matricule)
                        )'''
        )
        
        # Créer la table GeneratedCode avec la colonne Validité
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS code (
                                code_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                generated_code VARCHAR(10) NOT NULL,
                                generated_by VARCHAR(20) NOT NULL,
                                generated_at DATETIME NOT NULL,
                                expiration_date DATETIME NOT NULL
                        )'''
        )
        
    # Méthode pour ajouter, supprimer ou récupérer des informations sur les élèves
    def manage_students(self, action, matricule=None, password=None, nom=None, prenom=None, classe=None):
        # Vérifier l'action spécifiée
        if action not in ['add', 'remove', 'get']:
            print("Action invalide. Veuillez spécifier 'add' pour ajouter, 'remove' pour supprimer ou 'get' pour récupérer.")
            return
        
        # Crypter le mot de passe si un nouveau mot de passe est fourni
        if password:
            password_hash = generate_password_hash(password)
        else:
            password_hash = None

        # Traiter chaque action
        if action == 'add':             
            try:
                # Ajouter un nouvel élève
                self.cursor.execute('''INSERT INTO eleves (matricule, mot_de_passe, nom, prenom, classe)
                                    VALUES (?, ?, ?, ?, ?)''',
                                    (matricule, password_hash, nom, prenom, classe))
                print(f"Élève ajouté avec matricule {matricule}.")
            except sqlite3.IntegrityError as e:
                print(f"Erreur : {e}")

        elif action == 'remove':
            # Supprimer l'élève avec le matricule spécifié
            self.cursor.execute('''DELETE FROM eleves WHERE matricule = ?''', (matricule,))
            print(f"Élève avec matricule {matricule} supprimé.")

        elif action == 'get':
            # Récupérer les informations sur l'élève avec le matricule spécifié
            self.cursor.execute('''SELECT * FROM eleves WHERE matricule = ?''', (matricule,))
            student_infos = self.cursor.fetchone()
            if student_infos:
                student_info = {
                    'user_type': 'eleve',
                    'matricule': student_infos[0],
                    'mot_de_passe': student_infos[1],
                    'nom': student_infos[2],
                    'prenom': student_infos[3]
                    # autres champs ici si nécessaire
                }
                return student_info
            else:
                return None

        # Commit des modifications dans la base de données
        self.conn.commit()
   
    # Méthode pour ajouter, supprimer ou récupérer des informations sur les identifiants CNED des élèves
    def manage_cned_ids(self, action, eleve_matricules=None, identifiant_CNED=None, mot_de_passe_CNED=None):
        # Vérifier l'action spécifiée
        if action not in ['add', 'remove', 'get']:
            print("Action invalide. Veuillez spécifier 'add' pour ajouter, 'remove' pour supprimer ou 'get' pour récupérer.")
            return

        # Vérifier si eleve_matricules est une liste
        if not isinstance(eleve_matricules, list):
            eleve_matricules = [eleve_matricules]

        # Traiter chaque élève séparément
        for eleve_matricule in eleve_matricules:
            # Ajouter un identifiant CNED pour l'élève
            if action == 'add':
                try:
                    self.cursor.execute('''INSERT INTO id_cned (eleve_matricule, identifiant_CNED, mot_de_passe_CNED)
                                           VALUES (?, ?, ?)''',
                                        (eleve_matricule, identifiant_CNED, mot_de_passe_CNED))
                    print(f"Identifiant CNED ajouté pour l'élève avec matricule {eleve_matricule}.")
                except sqlite3.IntegrityError as e:
                    print(f"Erreur : {e}")

            # Supprimer l'identifiant CNED de l'élève
            elif action == 'remove':
                self.cursor.execute('''DELETE FROM id_cned WHERE eleve_matricule = ?''', (eleve_matricule,))
                print(f"Identifiant CNED supprimé pour l'élève avec matricule {eleve_matricule}.")

            # Récupérer les identifiants CNED de l'élève
            elif action == 'get':
                self.cursor.execute('''SELECT * FROM id_cned WHERE eleve_matricule = ?''', (eleve_matricule,))
                cned_ids = self.cursor.fetchone()
                if cned_ids:
                    # Construire un dictionnaire avec les informations de l'élève
                    eleve_info = {
                        'matricule': cned_ids[0],
                        'identifiant_CNED': cned_ids[1],
                        'mot_de_passe_CNED': cned_ids[2],
                    }
                    print(f"Informations de l'élève avec matricule {eleve_matricule} : {eleve_info}")
                else:
                    print(f"Aucun identifiant CNED trouvé pour l'élève avec matricule {eleve_matricule}.")

        # Commit les modifications dans la base de données
        self.conn.commit()

    
    # Méthode pour ajouter, supprimer ou récupérer un code généré pour un ou plusieurs élèves
    def manage_generated_codes(self, action, generated_code=None, generated_by=None, generated_at=None, expiration_date=None, code_id=None):
    # Vérifier l'action spécifiée
        if action not in ['add', 'remove', 'get']:
            print("Action invalide. Veuillez spécifier 'add' pour ajouter, 'remove' pour supprimer ou 'get' pour récupérer.")
            return
            
        # # Initialisez le curseur ici
        # self.cursor = self.conn.cursor()
        
        # Ajouter un code généré
        if action == 'add':
            try:
                self.cursor.execute('''INSERT INTO code (generated_code, generated_by, generated_at, expiration_date)
                                    VALUES (?, ?, ?, ?)''',
                                    (generated_code, generated_by, generated_at, expiration_date,))
                print("Code généré ajouté.")
            except sqlite3.Error as e:
                print("Erreur lors de l'ajout du code généré :", e)

        # Supprimer un code généré
        elif action == 'remove':
            try:
                self.cursor.execute('''DELETE FROM code WHERE code_id = ?''', (code_id,))
                print("Code généré supprimé.")
            except sqlite3.Error as e:
                print("Erreur lors de la suppression du code généré :", e)

        # Récupérer un code généré
        elif action == 'get':
            try:
                self.cursor.execute('''SELECT * FROM GeneratedCode WHERE code = ?''', (generated_code,))
                code = self.cursor.fetchone()
                if code:
                    generated_code_info = {
                        'code_id': code[0],
                        'generated_code': code[1],
                        'generated_by': code[2],
                        'generated_at': code[3],
                        'expiration_date': code[4],
                        'validite': code[5]
                    }
                    print("Informations du code généré :", generated_code_info)
                else:
                    print("Aucun code généré trouvé.")
            except sqlite3.Error as e:
                print("Erreur lors de la récupération du code généré :", e)
        
        # Commit les modifications dans la base de données
        self.conn.commit()
   

        
bdd = DatabaseManager()
with bdd:
    # Creation des table
    # bdd.create_tables()
    # bdd.manage_students('add', 'test', 'test', 'test', 'test', 'test')
    # bdd.manage_students('add', '123456', 'test', 'test', 'test', 'test')
    
    pass