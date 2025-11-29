from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from models.database import SessionLocal
from models.users import Usuario

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        db = SessionLocal()

        existente = db.query(Usuario).filter_by(email=email).first()
        if existente:
            flash("E-mail já registrado!", "danger")
            db.close()
            return redirect(url_for('auth_bp.register'))

        novo = Usuario(
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha) 
        )

        db.add(novo)
        db.commit()
        db.close()

        flash("Conta criada com sucesso!", "success")
        return redirect(url_for('auth_bp.login'))

    return render_template('register.html')

from flask_login import login_user

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        db = SessionLocal()
        usuario = db.query(Usuario).filter_by(email=email).first()

        if not usuario:
            flash("Usuário não encontrado!", "danger")
            db.close()
            return redirect(url_for('auth_bp.login'))

        if not check_password_hash(usuario.senha_hash, senha):
            flash("Senha incorreta!", "danger")
            db.close()
            return redirect(url_for('auth_bp.login'))

        login_user(usuario)

        flash("Login realizado!", "success")
        db.close()
        return redirect(url_for('controllers_bp.dashboard'))

    return render_template('login.html')

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))