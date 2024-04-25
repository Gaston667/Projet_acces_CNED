import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

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
        try:            
            # Création de la table des élèves
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS eleves (
                                    matricule TEXT NOT NULL PRIMARY KEY,
                                    mot_de_passe TEXT NOT NULL,
                                    identifiant_CNED TEXT NOT NULL,
                                    mot_de_passe_CNED TEXT NOT NULL,
                                    nom TEXT NOT NULL,
                                    prenom TEXT NOT NULL,
                                    classe TEXT NOT NULL
                                )'''
            )

            # Création de la table des codes générés
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS code (
                                    code_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    generated_code VARCHAR(10) NOT NULL,
                                    generated_at DATETIME NOT NULL,
                                    expiration_date DATETIME NOT NULL
                                )'''
            )

            # Création de la table de l'historique de génération de code
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS code_history (
                                    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    code_id INTEGER  NOT NULL,
                                    generated_at DATETIME NOT NULL,
                                    expiration_date DATETIME NOT NULL,
                                    FOREIGN KEY (code_id) REFERENCES code (code_id),
                                    FOREIGN KEY (generated_at) REFERENCES code (generated_at),
                                    FOREIGN KEY (expiration_date) REFERENCES code (expiration_date)
                                )'''
            )

        except sqlite3.Error as e:
            # En cas d'erreur, annuler la transaction et afficher l'erreur
            print("Erreur lors de la création des tables :", e)
            
    """
        La Partie de l'ajout de la gestion des éléments 
    """
    # Ajouter un élève
    def add_student(self, matricule, mot_de_passe, identifiant_CNED, mot_de_passe_CNED, nom, prenom, classe):
        # mot_de_passe = generate_password_hash(mot_de_passe)
        # mot_de_passe_CNED = generate_password_hash(mot_de_passe_CNED)
        try:
            self.cursor.execute('''INSERT INTO eleves (matricule, mot_de_passe, identifiant_CNED, mot_de_passe_CNED, nom, prenom, classe) 
                                VALUES (?, ?, ?, ?, ?, ?, ?)''', (matricule, mot_de_passe, identifiant_CNED, mot_de_passe_CNED, nom, prenom, classe))
            print("Élève ajouté avec succès.")
        except sqlite3.IntegrityError:
            print("Erreur : Un élève avec ce matricule existe déjà dans la base de données.")
        except sqlite3.Error as e:
            print("Erreur lors de l'ajout de l'élève :", e)

    # Rechercher un élève par matricule
    def get_student_by_matricule(self, matricule):
        try:
            self.cursor.execute("SELECT * FROM eleves WHERE matricule=?", (matricule,))
            student = self.cursor.fetchone()
            if student:
                # Convertir la ligne de la base de données en un dictionnaire
                student_dict = {
                    'matricule': student[0],
                    'mot_de_passe': student[1],
                    'identifiant_CNED': student[2],
                    'mot_de_passe_CNED': student[3],
                    'nom': student[4],
                    'prenom': student[5],
                    'classe': student[6]
                }
                return student_dict
            else:
                print("Aucun élève trouvé avec ce matricule.")
                return None
        except sqlite3.Error as e:
            print("Erreur lors de la récupération de l'élève par matricule:", e)
        return None
    
    # Rechercher un élément par nom
    def get_student_by_nom(self, nom):
        try:
            self.cursor.execute("SELECT * FROM eleves WHERE nom=?", (nom,))
            students = self.cursor.fetchall()
            if students:
                student_dicts = []
                for student in students:
                    student_dict = {
                        'matricule': student[0],
                        'mot_de_passe': student[1],
                        'identifiant_CNED': student[2],
                        'mot_de_passe_CNED': student[3],
                        'nom': student[4],
                        'prenom': student[5],
                        'classe': student[6]
                    }
                    student_dicts.append(student_dict)
                return student_dicts
            else:
                print("Aucun élève trouvé avec ce nom.")
                return 
        except sqlite3.Error as e:
            print("Erreur lors de la récupération des élèves par nom:", e)
            return 

    # Mettre à jour le mot de passe d'un élément
    def update_student_password(self, matricule, new_password):
        # new_password = generate_password_hash(new_password)
        try:
            self.cursor.execute("UPDATE eleves SET mot_de_passe=? WHERE matricule=?", (new_password, matricule))
            print("Mot de passe de l'élève mis à jour avec succès.")
        except sqlite3.Error as e:
            print("Erreur lors de la mise à jour du mot de passe de l'élève:", e)
            
    def update_student_cned_password(self, matricule, new_password):
        # new_password = generate_password_hash(new_password)
        try:
            self.cursor.execute("UPDATE eleves SET mot_de_passe_CNED=? WHERE matricule=?", (new_password, matricule))
            print("Mot de passe cned de l'élève mis à jour avec succès.")
        except sqlite3.Error as e:
            print("Erreur lors de la mise à jour du mot de passe de l'élève:", e)

    def delete_student(self, matricule):
        try:
            self.cursor.execute("DELETE FROM eleves WHERE matricule=?", (matricule,))
            if self.cursor.rowcount > 0:
                print("Élève supprimé avec succès.")
            else:
                print("Aucun élève trouvé avec ce matricule.")
        except sqlite3.Error as e:
            print("Erreur lors de la suppression de l'élève:", e)

    def get_all_students(self):
        try:
            # Exécuter une requête SQL pour sélectionner tous les élèves
            self.cursor.execute("SELECT * FROM eleves")
            
            # Récupérer tous les résultats de la requête
            students = self.cursor.fetchall()
            # Retourner la liste des élèves récupérés
            return students
        except Exception as e:
            # Gérer les exceptions
            print("Erreur lors de la récupération des élèves:", e)
            return None

    """
        La parite pour la gestion de CODE
    """
    
    def add_generated_code(self, generated_code,  generated_at, expiration_date):
        try:
            self.cursor.execute('''INSERT INTO code (generated_code, generated_at, expiration_date) 
                                VALUES (?, ?, ?)''', (generated_code,  generated_at, expiration_date))
            print("Code généré ajouté avec succès.")
        except sqlite3.Error as e:
            print("Erreur lors de l'ajout du code généré:", e)

    
   
    
    def get_generated_code(self, code):
        try:
            self.cursor.execute("SELECT * FROM code WHERE generated_code=?", (code,))
            codes = self.cursor.fetchall()
            if codes:
                code_dicts = []
                for code in codes:
                    code_dict = {
                        'id_code': code[0],
                        'generated_code': code[1],
                        'generated_at': code[2],
                        'expiration_date': code[3]
                    }
                    code_dicts.append(code_dict)
                return code_dicts
            else:
                print("Aucun code généré avec ce nom.")
                return 
        except sqlite3.Error as e:
            print("Erreur lors de la sélection du code généré:", e)
            return 

       
bdd = DatabaseManager()
with bdd:
    # Creation des table
    # bdd.create_tables()
    # bdd.add_student('1234', 'ok', 'john.doe', 'ok', 'John', 'Doe', '5e')
    # bdd.add_student('5678', 'ok', 'jane.doe', 'ok', 'Jane', 'Doe', '5e')
    # bdd.update_student_password('5678', 'ok')
    # bdd.delete_student('1234')
    # bdd.delete_student('5678')
    pass