import tkinter as tk
from tkinter import ttk, Toplevel
import requests, time, os
from tkinter import messagebox
from selenium import webdriver

class LoginWindow:
    def __init__(self):
        self.session_data = {}  # Ajout de l'attribut session_data initialisé à un dictionnaire vide
        self.root_login = tk.Tk()
        self.root_login.title("Authentification")
        self.root_login.configure(bg='#333333')
        # root_code_entry.geometry("440x190")
   
        
        # Obtention de la taille de l'écran
        screen_width = self.root_login.winfo_screenwidth()
        screen_height = self.root_login.winfo_screenheight()
        # Définition de la taille de la fenêtre pour qu'elle occupe tout l'écran
        self.root_login.geometry("%dx%d+0+0" % (screen_width, screen_height))
        
        self.Frame = tk.Frame(self.root_login, bg='#333333')
        self.create_widgets()

    def create_widgets(self):
        self.login_label  = tk.Label(self.Frame, text="Connexion", bg='#333333', fg='#ff3399', font=("Arial", 30))
        self.matricule_label = tk.Label(self.Frame, text='Matricule', bg='#333333', fg='#ffffff', font=("Arial", 16))
        self.matricule_entry = tk.Entry(self.Frame, font=("Arial", 16))
        self.password_entry = tk.Entry(self.Frame, show="*", font=("Arial", 16))
        self.password_label = tk.Label(self.Frame, text="Mot de passe", bg='#333333', fg='#ffffff', font=("Arial", 16))
        self.login_button = tk.Button(self.Frame, text="se connecter", command=self.login, fg='#ffffff', bg='#ff3399', height=1, bd=1, font=("Arial", 16))
        self.show_password = tk.BooleanVar()  # Variable de contrôle pour suivre l'état du bouton
        self.show_password_checkbox = tk.Checkbutton(self.Frame, text="Afficher le mot de passe", variable=self.show_password, onvalue=True, offvalue=False, command=self.toggle_password_visibility, bg='#333333', fg='#ffffff', font=("Arial", 12))

        self.login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
        self.matricule_label.grid(row=1, column=0)
        self.matricule_entry.grid(row=1, column=1, pady=20)
        self.password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1, pady=20)
        self.show_password_checkbox.grid(row=3, column=0, columnspan=2, pady=10)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=30)

        self.Frame.place(relx=0.5, y=350, anchor=tk.CENTER)

    def login(self):
        matricule = self.matricule_entry.get()
        password = self.password_entry.get() 
        
        response = requests.post('http://127.0.0.1:5000/login', json={'matricule': matricule, 'password': password})
        response_json = response.json()
        
        if response.status_code == 200:
            messagebox.showinfo("Succès", response_json['message'])
            self.session_data = response_json.get('session_data', {})  # Stockage des données de session
            self.root_login.destroy()
            code_entry_window = CodeEntryWindow(self.session_data)  # Passage de session_data à CodeEntryWindow
        elif response.status_code == 401:
            messagebox.showerror("Erreur", f"{response_json['message']}. Veuillez réessayer.")
        else:
            messagebox.showerror("Erreur", "Une erreur s'est produite. Verifier votre connexion")

    def toggle_password_visibility(self):
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")


class CodeEntryWindow:
    def __init__(self, session_data):
        self.session_data = session_data
        self.root_code_entry = tk.Tk()
        self.root_code_entry.title("Entrer le code")
        self.root_code_entry.configure(bg='#333333')
        # root_code_entry.geometry("440x190")
        
        # Obtention de la taille de l'écran
        screen_width = self.root_code_entry.winfo_screenwidth()
        screen_height = self.root_code_entry.winfo_screenheight()
        # Définition de la taille de la fenêtre pour qu'elle occupe tout l'écran
        self.root_code_entry.geometry("%dx%d+0+0" % (screen_width, screen_height))
        
        
        self.Frame = tk.Frame(self.root_code_entry, bg='#333333')
        self.create_widgets()

    def create_widgets(self):
        session = self.session_data 
        self.nameofuser = tk.Label(self.Frame, text=f"USER: {session['user']['nom']}.{session['user']['prenom']}", bg='#333333', fg='#ff3399', font=("Arial", 30))
        self.titre = tk.Label(self.Frame, text="Entrer le code fourni par le surveillant", bg='#333333', fg='#ff3399', font=("Arial", 30))
        self.label_code = tk.Label(self.Frame, text='CODE :', bg='#333333', fg='#ffffff', font=("Arial", 16))
        self.entry_code = tk.Entry(self.Frame, font=("Arial", 16))
        self.button_submit_code = tk.Button(self.Frame, text="Soumettre le code", fg='#ffffff', bg='#ff3399', height=1, bd=1, font=("Arial", 16), command=self.submit_code)
        
        self.nameofuser.grid(row=0, column=0, columnspan=2, sticky="news", pady=10)  # Ajustement du padding
        self.titre.grid(row=1, column=0, columnspan=2, sticky="news", pady=10)  # Ajustement du padding
        self.label_code.grid(row=2, column=0, pady=10)  # Ajustement du row
        self.entry_code.grid(row=2, column=1, pady=10)  # Ajustement du row
        self.button_submit_code.grid(row=3, column=0, columnspan=2, pady=10)  # Ajustement du padding
        self.Frame.place(relx=0.5, y=300, anchor=tk.CENTER)

    def submit_code(self):
        code = self.entry_code.get()
        
        response = requests.post('http://127.0.0.1:5000/verifcode', json={'code': code, 'session_data': self.session_data})
        response_json = response.json()
        if response.status_code == 200:
            messagebox.showinfo("Succès", response_json['message'] + "\n VEUILLEZ ATTENDRE L'OUVERTURE DE LA PAGE CNED....")
            self.root_code_entry.destroy()
            self.open_browser()
        elif response.status_code == 400:
            messagebox.showerror("Erreur", response_json['message'])
       
    def open_browser(self):
        session = self.session_data 
        # Code pour récupérer les informations de l'utilisateur et remplir les champs du formulaire CNED
        identifiant_cned = session['user']['identifiant_CNED']
        mot_de_passe_cned = session['user']['mot_de_passe_CNED']
                                           
        #Creer une variable qui pour declancher le navigateur
        #diver_path est le chemin vers le chromedriver
        drver_path = "chromedriver.exe"
        try:
            driver = webdriver.Chrome()
                    
            # url vers la page d'acceuille du CNED
            # url = "https://www.cned360.fr/uPortal/p/home"
            # url vers la page de connexion du CNED
            url = "https://sts.cned.fr/adfs/ls/?wtrealm=https%3A%2F%2Fespaceinscrit.cned.fr&wctx=WsFedOwinState%3D1kJs2CMiqSTWgXUULhuPNagdvV-hz-c0o_YiPEvrc0TVYGnFCjzdXTjK607t2ugcX3LlaTG5zwr1FJY85ayG05QkW5XnQqmD5haiXJCmkIXf7L6jrYh0Hd1zJO5CVObkEVFqF0xYunS-fZboGWE2SyIv_373XDJ2P4CAoqKdSx4&wa=wsignin1.0"
                          
            
            # Ouvrir la page de connexion CNED
            driver.get(url)  
            # time.sleep(4)    
            # driver.close()
                    
            # Remplir les champs du formulaire de connexion CNED avec les informations de l'utilisateur
            identifiant_input = driver.find_element('name', 'UserName')
            identifiant_input.send_keys(identifiant_cned)
            mot_de_passe_input = driver.find_element('name','Password')
            mot_de_passe_input.send_keys(mot_de_passe_cned)  
                       
            # Soumettre le formulaire de connexion CNED
            submit_button = driver.find_element('id','submitButton')
            submit_button.click()
              
            # time.sleep(5)
                    
            # Récupérer le processus WebDriver
            webdriver_process = driver.service.process
            # Obtenez le pid du processus du pilote WebDriver
            webdriver_process_name = webdriver_process.pid
            
            
            # Tuer le processus WebDriver
            print("taskkill /f /pid {}".format(webdriver_process_name))
            os.system("taskkill /f /pid {}".format(webdriver_process_name))
            messagebox.showerror("Succès", "Connexion reussi")
        except Exception as e:
            # Terminer
            messagebox.showerror("Erreur", "Imposible d'ouvrire le navigatuer ou de remplir les champs: \
                                 \n \n 1. Verifier votre connexion internet (vos câbles réseau, votre modem et vos routeurs) \n 2.Verifier votre parfeu ou votre proxy")
        finally:
            driver.quit()


if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.root_login.mainloop()