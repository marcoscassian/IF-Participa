from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.reclamacoes import Reclamacao
from models.sugestoes import Sugestao
from models.database import db_session, SessionLocal

#blueprint de rotas do usuário no sistema
user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/meu-perfil")
@login_required
def meu_perfil():
    db = SessionLocal()
    minhas_reclamacoes = db.query(Reclamacao).filter_by(autor_id=current_user.id).all()
    minhas_sugestoes = db.query(Sugestao).filter_by(autor_id=current_user.id).all()

    return render_template(
        "user/meu_perfil.html",
        usuario=current_user,
        reclamacoes=minhas_reclamacoes,
        sugestoes=minhas_sugestoes
    )