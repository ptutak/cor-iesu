from flask import Blueprint, redirect, render_template, request, url_for, g

from cor_iesu.auth import login_required

from .models import db, PeriodAssignment

api = Blueprint("views", __name__)


@api.route("/", methods=("GET", "POST", "DELETE"))
@login_required
def user():
    return render_template("user.html")


@api.route("/assignments", methods=("GET", "POST"))
def assignments():
    if request.method == "GET":
        g.empty_assignments = (
            db.session.query(PeriodAssignment)
            .join
        )
        # join with collecion, filter by enabled collections, then filter by assignments
    #     g.hours = (
    #     db.session.query(models.Hour)
    #     .join(models.Hour.periods)
    #     .join(models.Hour.assignments, isouter=True)
    #     .filter(models.Period.collection == g.collection)
    #     .order_by(models.Hour.weekday)
    #     .order_by(models.Hour.hour)
    #     .all()
    # )
        return render_template("assignments.html")

    return redirect(url_for("views.assignments"))
