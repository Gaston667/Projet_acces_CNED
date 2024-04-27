from flask import Flask, render_template, request, redirect, url_for, session
from auth import auth_blueprint
from eleves import eleves_blueprint 
from supervisor import supervisor_blueprint

app = Flask(__name__)   
app.config['SECRET_KEY'] = b'Tl\xa3d\xc7Ey\xdf`\xd6\x04\x9e\x14\xa5\xa7?'


    
# Enregistrement des Blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(eleves_blueprint)
app.register_blueprint(supervisor_blueprint)


# Lancement du serveur
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


