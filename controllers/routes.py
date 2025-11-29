from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.reclamacoes import Reclamacao
from models.sugestoes import Sugestao
from models.database import db_session, SessionLocal

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

@controllers_bp.route("/meu-perfil")
@login_required
def meu_perfil():
    db = SessionLocal()

    minhas_reclamacoes = db.query(Reclamacao).filter_by(autor_id=current_user.id).all()
    minhas_sugestoes = db.query(Sugestao).filter_by(autor_id=current_user.id).all()

    return render_template(
        "meu_perfil.html",
        usuario=current_user,
        reclamacoes=minhas_reclamacoes,
        sugestoes=minhas_sugestoes
    )

@controllers_bp.route("/reclamacao/<int:id>/excluir")
@login_required
def excluir_reclamacao(id):
    db = SessionLocal()
    rec = db.query(Reclamacao).filter_by(id=id, autor_id=current_user.id).first()

    if not rec:
        flash("Reclamação não encontrada ou não é sua.")
        return redirect(url_for("controllers_bp.meu_perfil"))

    db.delete(rec)
    db.commit()
    flash("Reclamação excluída com sucesso.")
    return redirect(url_for("controllers_bp.meu_perfil"))

@controllers_bp.route("/sugestao/<int:id>/excluir")
@login_required
def excluir_sugestao(id):
    db = SessionLocal()
    sug = db.query(Sugestao).filter_by(id=id, autor_id=current_user.id).first()

    if not sug:
        flash("Sugestão não encontrada ou não é sua.")
        return redirect(url_for("controllers_bp.meu_perfil"))

    db.delete(sug)
    db.commit()
    flash("Sugestão excluída com sucesso.")
    return redirect(url_for("controllers_bp.meu_perfil"))

@controllers_bp.route("/reclamacao/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_reclamacao(id):
    db = SessionLocal()
    rec = db.query(Reclamacao).filter_by(id=id, autor_id=current_user.id).first()

    if not rec:
        flash("Reclamação não encontrada ou não é sua.")
        return redirect(url_for("controllers_bp.meu_perfil"))

    if request.method == "POST":
        rec.titulo = request.form["titulo"]
        rec.descricao = request.form["descricao"]
        db.commit()
        flash("Reclamação atualizada.")
        return redirect(url_for("controllers_bp.meu_perfil"))

    return render_template("editar_reclamacao.html", reclamacao=rec)

@controllers_bp.route("/sugestao/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_sugestao(id):
    db = SessionLocal()
    sug = db.query(Sugestao).filter_by(id=id, autor_id=current_user.id).first()

    if not sug:
        flash("Sugestão não encontrada ou não é sua.")
        return redirect(url_for("controllers_bp.meu_perfil"))

    if request.method == "POST":
        sug.titulo = request.form["titulo"]
        sug.descricao = request.form["descricao"]
        db.commit()
        flash("Sugestão atualizada.")
        return redirect(url_for("controllers_bp.meu_perfil"))

    return render_template("editar_sugestao.html", sugestao=sug)
