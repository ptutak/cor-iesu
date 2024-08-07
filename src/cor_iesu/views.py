from flask import Blueprint, g, redirect, render_template, request, url_for

from cor_iesu.auth import login_required

from .models import Collection, PeriodCollection, db

api = Blueprint("views", __name__)


@api.route("/", methods=("GET", "POST", "DELETE"))
@login_required
def user():
    return render_template("user.html")


@api.route("/assignments", methods=("GET", "POST"))
def assignments():
    if request.method == "GET":
        period_collections = (
            db.session.query(PeriodCollection)
            .join(PeriodCollection.collection)
            .join(PeriodCollection.assignments, isouter=True)
            .filter(Collection.enabled == True)
            .all()
        )
        g.empty_assignments = [
            period_collection for period_collection in period_collections if len(period_collection.assignments) < 2
        ]
        return render_template("assignments.html")

    return redirect(url_for("views.assignments"))
