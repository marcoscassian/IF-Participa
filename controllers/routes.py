from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.reclamacoes import Reclamacao
from models.sugestoes import Sugestao
from models.database import db_session

controllers_bp = Blueprint("controllers_bp", __name__)

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

@controllers_bp.route("/enviar-sugestao", methods=["GET", "POST"])
@login_required
def enviar_sugestao():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]

        nova = Sugestao(
            titulo=titulo,
            descricao=descricao,
            autor_id=current_user.id
        )

        db_session.add(nova)
        db_session.commit()

        return redirect(url_for("controllers_bp.dashboard"))

    return render_template("enviar_sugestao.html")

@controllers_bp.route("/enviar-reclamacao", methods=["GET", "POST"])
@login_required
def enviar_reclamacao():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]

        nova = Reclamacao(
            titulo=titulo,
            descricao=descricao,
            autor_id=current_user.id
        )

        db_session.add(nova)
        db_session.commit()

        return redirect(url_for("controllers_bp.dashboard"))

    return render_template("enviar_reclamacao.html")