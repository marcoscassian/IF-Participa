from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.reclamacoes import Reclamacao
from models.sugestoes import Sugestao
from models.database import db_session, SessionLocal
from controllers.routes import controllers_bp
from controllers.user import user_bp

#blueprint de rotas gerais do sistema
reclamacoes_bp = Blueprint("reclamacoes_bp", __name__)

#enviar reclamação
@reclamacoes_bp.route("/enviar-reclamacao", methods=["GET", "POST"])
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

    return render_template("reclamacoes/enviar_reclamacao.html")

#excluir reclamação
@reclamacoes_bp.route("/reclamacao/<int:id>/excluir")
@login_required
def excluir_reclamacao(id):
    db = SessionLocal()
    rec = db.query(Reclamacao).filter_by(id=id, autor_id=current_user.id).first()

    if not rec:
        flash("Reclamação não encontrada ou não é sua.")
        return redirect(url_for("user_bp.meu_perfil"))

    db.delete(rec)
    db.commit()
    flash("Reclamação excluída com sucesso.")
    return redirect(url_for("user_bp.meu_perfil"))

#editar reclamação
@reclamacoes_bp.route("/reclamacao/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_reclamacao(id):
    db = SessionLocal()
    rec = db.query(Reclamacao).filter_by(id=id, autor_id=current_user.id).first()

    if not rec:
        flash("Reclamação não encontrada ou não é sua.")
        return redirect(url_for("user_bp.meu_perfil"))

    if request.method == "POST":
        rec.titulo = request.form["titulo"]
        rec.descricao = request.form["descricao"]
        db.commit()
        flash("Reclamação atualizada.")
        return redirect(url_for("user_bp.meu_perfil"))

    return render_template("reclamacoes/editar_reclamacao.html", reclamacao=rec)