import random
import string
# from database import DatabaseManager

# Fonction pour générer le code
def generate_code():
    lettres = ''.join(random.choices(string.ascii_uppercase, k=2))
    chiffres = ''.join(random.choices(string.digits, k=4))
    return lettres + chiffres

def gerer_casse(chaine, mode):
    """
    Gère la casse d'une chaîne de caractères selon le mode spécifié.

    Args:
        chaine (str): La chaîne de caractères à gérer.
        mode (str): Le mode de gestion de la casse ('majuscules', 'minuscules' ou 'premiere_lettre').

    Returns:
        str: La chaîne de caractères modifiée selon le mode spécifié.
    """
    if mode == 'majuscules':
        return chaine.upper()
    elif mode == 'minuscules':
        return chaine.lower()
    elif mode == 'premiere_lettre':
        return chaine.capitalize()
    else:
        return chaine  # Retourne la chaîne inchangée si le mode n'est pas reconnu

def generate_matricule():
    # Lettres possibles pour le préfixe
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Choix aléatoire d'une lettre pour le préfixe
    prefix = ''.join(random.choices(letters, k=2))
    # Générer un nombre aléatoire entre 10 et 99 pour le suffixe du matricule
    suffix = str(random.randint(10, 99))
    # Concaténez le préfixe et le suffixe pour former le matricule
    matricule = prefix + suffix
    return matricule

def generate_password():
    # Générer un mot de passe aléatoire de longueur 8 avec des lettres et des chiffres
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    return password


