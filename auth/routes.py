from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from models.database import SessionLocal
from models.users import Usuario

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')


# --- PÁGINA DE CADASTRO ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        db = SessionLocal()

        # Verifica se o email já existe
        existente = db.query(Usuario).filter_by(email=email).first()
        if existente:
            flash("E-mail já registrado!", "danger")
            db.close()
            return redirect(url_for('auth_bp.register'))

        # CRIA o usuário
        novo = Usuario(
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha)  # ← CORRETO!
        )

        db.add(novo)
        db.commit()
        db.close()

        flash("Conta criada com sucesso!", "success")
        return redirect(url_for('auth_bp.login'))

    return render_template('register.html')


# --- PÁGINA DE LOGIN ---
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

        flash("Login realizado!", "success")
        db.close()
        return redirect(url_for('index'))

    return render_template('login.html')
