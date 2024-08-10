from collections import namedtuple

from flask import Blueprint, abort, g, redirect, render_template, request, url_for
from sqlalchemy import select

from cor_iesu.auth import login_required

from .const import DatabaseKeys, DefaultValues
from .models import (
    Collection,
    CollectionConfig,
    Period,
    PeriodAssignment,
    PeriodCollection,
    db,
)

api = Blueprint("views", __name__)


@api.route("/", methods=("GET", "POST", "DELETE"))
@login_required
def user():
    return render_template("user.html.jinja2")


@api.route("/assignments", methods=("GET", "POST"))
def assignments():
    collections_configs = db.session.execute(
        select(CollectionConfig)
        .join(Collection)
        .where(Collection.enabled)
        .where(CollectionConfig.name == DatabaseKeys.ASSIGNMENT_LIMIT)
    ).all()
    limit_per_collection = {config.collection.id: int(config.value) for config in collections_configs}

    if request.method == "GET":
        period_collections = db.session.execute(
            select(PeriodCollection, Collection, Period, PeriodAssignment)
            .join(PeriodCollection.collection)
            .join(PeriodCollection.period)
            .join(PeriodCollection.assignments, isouter=True)
            .where(Collection.enabled)
        ).all()

        free_assignment = namedtuple("free_assignment", ["collection_id", "period_collection_id", "period_name"])

        g.free_assignments = [
            free_assignment(
                collection_id=row.Collection.id,
                period_name=row.Period.name,
                period_collection_id=row.PeriodCollection.id,
            )
            for row in period_collections
            if len(row.PeriodCollection.assignments)
            < limit_per_collection.get(
                row.PeriodCollection.collection.id,
                g.config.get(DatabaseKeys.ASSIGNMENT_LIMIT, DefaultValues.ASSIGNMENT_LIMIT),
            )
        ]

        g.available_collections = db.session.scalars(select(Collection).where(Collection.enabled)).all()

        return render_template("assignments.html.jinja2")

    form = request.form.to_dict()
    form_fields_required = {"collection-select", "period-select", "first-name", "last-name"}
    if not form_fields_required.issubset(form.keys()):
        return abort(400, f"You have to provide the following form fields: {form_fields_required}")

    if "email" not in form and "phone-number" not in form:
        return abort(400, "You have to provide one of those form fields: 'email', 'phone-number'")

    with db.session.begin():
        period_collection_id = int(form["period-select"])
        collection_id = int(form["collection-select"])
        first_name = form["first-name"]
        last_name = form["last-name"]
        email = None
        phone_number = None
        if "email" in form:
            email = form["email"]
        else:
            phone_number = form["phone-number"]

        period_collections = db.session.execute(
            select(PeriodCollection, PeriodAssignment)
            .join(PeriodCollection.assignments, isouter=True)
            .where(PeriodCollection.id == period_collection_id)
        ).all()

        if len(period_collections) < limit_per_collection.get(
            collection_id,
            g.config.get(DatabaseKeys.ASSIGNMENT_LIMIT, DefaultValues.ASSIGNMENT_LIMIT),
        ):
            new_assignment = PeriodAssignment()
            new_assignment.id_period_collection = period_collection_id
            new_assignment.attendant_email = email
            new_assignment.attendant_phone_number = phone_number
            new_assignment.attendant_name = f"{first_name} {last_name}"
            db.session.add(new_assignment)

    return redirect(url_for("views.assignments"))
