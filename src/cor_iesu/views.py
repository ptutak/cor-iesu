from flask import Blueprint, abort, g, render_template, request
from sqlalchemy import func

from cor_iesu.auth import login_required
from cor_iesu.models import db

from . import models
from .const import ConfigKeys

api = Blueprint("views", __name__)


@api.route("/", methods=("GET", "POST", "DELETE"))
@login_required
def user():

    return render_template("user.html")
