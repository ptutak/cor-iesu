from sqlalchemy import select
from flask import Blueprint, g, redirect, render_template, request, url_for
from collections import namedtuple
from cor_iesu.auth import login_required

from .const import DatabaseKeys, DefaultValues
from .models import Collection, CollectionConfig, PeriodAssignment, PeriodCollection, Period, db

api = Blueprint("views", __name__)


@api.route("/", methods=("GET", "POST", "DELETE"))
@login_required
def user():
    return render_template("user.html.jinja2")


@api.route("/assignments", methods=("GET", "POST"))
def assignments():
    if request.method == "GET":
        collections_configs = (
            db.session.execute(
                select(CollectionConfig)
                .join(Collection)
                .where(Collection.enabled)
                .where(CollectionConfig.name == DatabaseKeys.ASSIGNMENT_LIMIT)
            ).all()
        )
        print(collections_configs)

        limit_per_collection = {config.collection.name: int(config.value) for config in collections_configs}

        period_collections = (
            db.session.execute(
                select(PeriodCollection, Collection, Period, PeriodAssignment)
                .join(PeriodCollection.collection)
                .join(PeriodCollection.period)
                .join(PeriodCollection.assignments, isouter=True)
                .where(Collection.enabled)
            ).all()
        )
        free_assignment = namedtuple("free_assignment", ["collection_id", "period_name", "period_id"])
        g.free_assignments = [
            free_assignment(collection_id=row.Collection.id, period_name=row.Period.name, period_id=row.Period.id)
            for row in period_collections
            if len(row.PeriodCollection.assignments)
            < limit_per_collection.get(
                row.PeriodCollection.collection.name,
                g.config.get(DatabaseKeys.ASSIGNMENT_LIMIT, DefaultValues.ASSIGNMENT_LIMIT),
            )
        ]

        g.available_collections = (
            db.session.scalars(select(Collection).where(Collection.enabled)).all()
        )

        print(g.available_collections)
        for collection in g.available_collections:
            print(collection.id, collection.enabled, collection.name)
        return render_template("assignments.html.jinja2")

    return redirect(url_for("views.assignments"))
