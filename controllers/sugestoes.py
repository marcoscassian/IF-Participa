from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.reclamacoes import Reclamacao
from models.sugestoes import Sugestao
from models.database import db_session, SessionLocal
from controllers.routes import controllers_bp

#blueprint de rotas gerais do sistema
sugestoes_bp = Blueprint("sugestoes_bp", __name__)

#página principal do usuário logado
@sugestoes_bp.route("/dashboard")
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

#enviar sugestão
@sugestoes_bp.route("/enviar-sugestao", methods=["GET", "POST"])
@login_required
def enviar_sugestao():
    if request.method == "POST":
        nova = Sugestao(
            titulo=request.form["titulo"],
            descricao=request.form["descricao"],
            autor_id=current_user.id
        )
        db_session.add(nova)
        db_session.commit()
        return redirect(url_for("controllers_bp.dashboard"))

    return render_template("sugestoes/enviar_sugestao.html")

#excluir sugestão
@sugestoes_bp.route("/sugestao/<int:id>/excluir")
@login_required
def excluir_sugestao(id):
    db = SessionLocal()
    sug = db.query(Sugestao).filter_by(id=id, autor_id=current_user.id).first()

    if not sug:
        flash("Sugestão não encontrada ou não é sua.")
        return redirect(url_for("user_bp.meu_perfil"))

    db.delete(sug)
    db.commit()
    flash("Sugestão excluída com sucesso.")
    return redirect(url_for("user_bp.meu_perfil"))

#editar sugestão
@sugestoes_bp.route("/sugestao/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_sugestao(id):
    db = SessionLocal()
    sug = db.query(Sugestao).filter_by(id=id, autor_id=current_user.id).first()

    if not sug:
        flash("Sugestão não encontrada ou não é sua.")
        return redirect(url_for("user_bp.meu_perfil"))

    if request.method == "POST":
        sug.titulo = request.form["titulo"]
        sug.descricao = request.form["descricao"]
        db.commit()
        flash("Sugestão atualizada.")
        return redirect(url_for("user_bp.meu_perfil"))

    return render_template("sugestoes/editar_sugestao.html", sugestao=sug)