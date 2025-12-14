from flask import Flask, render_template
from flask_login import LoginManager

#importação dos modelos e criação das tabelas
from models import criar_tabelas
from models.users import Usuario
from models.database import SessionLocal

#importação dos blueprints (módulos de rotas)
from auth.routes import auth_bp 
from controllers.routes import controllers_bp
from controllers.user import user_bp
from controllers.sugestoes import sugestoes_bp
from controllers.reclamacoes import reclamacoes_bp

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
app.register_blueprint(user_bp)
app.register_blueprint(sugestoes_bp)
app.register_blueprint(reclamacoes_bp)

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
