from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.reclamacoes import Reclamacao
from models.sugestoes import Sugestao
from models.database import db_session, SessionLocal

#blueprint de rotas gerais do sistema
controllers_bp = Blueprint("controllers_bp", __name__)

#página principal do usuário logado
@controllers_bp.route("/dashboard")
@login_required
def dashboard():
    reclamacoes = db_session.query(Reclamacao).all()
    sugestoes = db_session.query(Sugestao).all()

    return render_template(
        "dashboard.html",
        usuario=current_user,
        reclamacoes=reclamacoes,
        sugestoes=sugestoes
    )

#página "Sobre"
@controllers_bp.route("/sobre", methods=["GET", "POST"])
@login_required
def sobre():
    return render_template("sobre.html")
