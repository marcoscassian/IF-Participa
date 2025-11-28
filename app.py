from flask import Flask, render_template
from flask_login import LoginManager
from models import criar_tabelas
from models.users import Usuario
from models.database import SessionLocal
from auth.routes import auth_bp 
from controllers.routes import controllers_bp

app = Flask(__name__)
app.secret_key = "CHAVE_ULTRA_SECRETA"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_bp.login"

app.register_blueprint(auth_bp)
app.register_blueprint(controllers_bp)


criar_tabelas()

@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    from models.users import Usuario
    user = db.query(Usuario).get(int(user_id))
    db.close()
    return user


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
