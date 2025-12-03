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

#enviar sugestão
@controllers_bp.route("/enviar-sugestao", methods=["GET", "POST"])
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

    return render_template("enviar_sugestao.html")

#enviar reclamação
@controllers_bp.route("/enviar-reclamacao", methods=["GET", "POST"])
@login_required
def enviar_reclamacao():
    if request.method == "POST":
        nova = Reclamacao(
            titulo=request.form["titulo"],
            descricao=request.form["descricao"],
            autor_id=current_user.id
        )
        db_session.add(nova)
        db_session.commit()
        return redirect(url_for("controllers_bp.dashboard"))

    return render_template("enviar_reclamacao.html")

#página de perfil do usuário
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

#excluir reclamação
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

#excluir sugestão
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

#editar reclamação
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

#editar sugestão
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

#página "Sobre"
@controllers_bp.route("/sobre", methods=["GET", "POST"])
@login_required
def sobre():
    return render_template("sobre.html")
