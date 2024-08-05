from flask import Blueprint, render_template, request, redirect, url_for

from cor_iesu.auth import login_required

api = Blueprint("views", __name__)


@api.route("/", methods=("GET", "POST", "DELETE"))
@login_required
def user():
    return render_template("user.html")


@api.route("/assignments", methods=("GET", "POST"))
def assignments():
    if request.method == "GET":
        return render_template("assignments.html")

    username = request.form["username"]
    password = request.form["password"]
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    phone_number = request.form["phone-number"]

    return redirect(url_for("views.assignments"))
