from flask import Blueprint, g, redirect, render_template, request, url_for

from cor_iesu.auth import login_required

from .const import DatabaseKeys, DefaultValues
from .models import Collection, CollectionConfig, Config, PeriodCollection, db

api = Blueprint("views", __name__)


@api.route("/", methods=("GET", "POST", "DELETE"))
@login_required
def user():
    return render_template("user.html")


@api.route("/assignments", methods=("GET", "POST"))
def assignments():
    if request.method == "GET":
        collections_configs = (
            db.session.query(CollectionConfig)
            .join(Collection)
            .filter(Collection.enabled == True)
            .filter(CollectionConfig.name == DatabaseKeys.ASSIGNMENT_LIMIT)
            .all()
        )

        limit_per_collection = {config.collection.name: int(config.value) for config in collections_configs}

        period_collections = (
            db.session.query(PeriodCollection)
            .join(PeriodCollection.collection)
            .join(PeriodCollection.assignments, isouter=True)
            .filter(Collection.enabled == True)
            .all()
        )
        g.empty_assignments = [
            period_collection
            for period_collection in period_collections
            if len(period_collection.assignments)
            < limit_per_collection.get(
                period_collection.collection.name,
                g.config.get(DatabaseKeys.ASSIGNMENT_LIMIT, DefaultValues.ASSIGNMENT_LIMIT),
            )
        ]

        g.available_collections = (
            db.session.query(Collection).filter(Collection.enabled == True)
        )
        return render_template("assignments.html")

    return redirect(url_for("views.assignments"))
