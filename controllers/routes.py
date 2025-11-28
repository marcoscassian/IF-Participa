from flask import Blueprint, render_template
from flask_login import login_required, current_user

controllers_bp = Blueprint("controllers_bp", __name__)

@controllers_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", usuario=current_user)
