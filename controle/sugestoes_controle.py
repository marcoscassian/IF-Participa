from flask import Blueprint, render_template, request, redirect, flash
from models.database import SessionLocal
from models.propostas import Proposta

sugestoes_controle = Blueprint("sugestoes_controle", __name__)



@sugestoes_controle.route("/sugestoes", methods=["GET", "POST"])
def sugestoes():
    db = SessionLocal()

 
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descricao = request.form.get("descricao")

        nova = Proposta(titulo=titulo, descricao=descricao)
        db.add(nova)
        db.commit()
        flash("Sugestão cadastrada com sucesso!", "success")
        return redirect("/sugestoes")

  
    lista = db.query(Proposta).all()
    return render_template("sugestoes.html", lista=lista)


@sugestoes_controle.route("/sugestoes/remover/<int:id>")
def remover(id):
    db = SessionLocal()
    item = db.query(Proposta).filter_by(id=id).first()

    if item:
        db.delete(item)
        db.commit()
        flash("Sugestão removida!", "info")

    return redirect("/sugestoes")
