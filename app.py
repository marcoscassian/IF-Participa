from flask import Flask, render_template
from flask_login import LoginManager
from models import criar_tabelas
from models.users import Usuario
from models.database import SessionLocal
from auth.routes import auth_bp 
from controllers.routes import controllers_bp

#criação da aplicação Flask
app = Flask(__name__)
app.secret_key = "CHAVE_ULTRA_SECRETA"  #usada para sessões e login

#configuração do sistema de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_bp.login"  #página padrão de login

#registro dos blueprints (módulos separados)
app.register_blueprint(auth_bp)
app.register_blueprint(controllers_bp)

#criar tabelas no banco de dados, caso não existam
criar_tabelas()

#função que carrega o usuário logado pela ID
@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    user = db.query(Usuario).get(int(user_id))
    db.close()
    return user

#rota principal
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
