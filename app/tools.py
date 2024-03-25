import random
import string

# Fonction pour générer le code
def generate_code():
    lettres = ''.join(random.choices(string.ascii_uppercase, k=2))
    chiffres = ''.join(random.choices(string.digits, k=4))
    return lettres + chiffres