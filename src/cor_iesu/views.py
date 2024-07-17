from flask import Blueprint, render_template

from cor_iesu.auth import login_required

api = Blueprint("views", __name__)


@api.route("/", methods=("GET", "POST", "DELETE"))
@login_required
def user():
    return render_template("user.html")
