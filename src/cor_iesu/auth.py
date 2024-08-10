import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from .models import Config, User, db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password = request.form["password"]
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    phone_number = request.form["phone-number"]

    error: str | None = None

    if not first_name:
        error = "Imie jest wymagane"
    elif not last_name:
        error = "Nazwisko jest wymagane"
    elif not phone_number:
        error = "Numer telefonu jest wymagany"
    elif not username:
        error = "Nazwa uzytkownika jest wymagana"
    elif not password:
        error = "Haslo jest wymagane"

    user: User | None = User.query.filter_by(username=username).first()

    if user is not None:
        error = "Dana osoba jest juz zarejestrowana"

    if error is not None:
        flash(error)

    session.clear()
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        username=username,
        password=generate_password_hash(password),
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("auth.login"))


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]
    error: str | None = None

    user: User | None = User.query.filter_by(username=username).first()

    if user is None:
        error = "Podana osoba nie jest zarejestrowana"
    elif not check_password_hash(user.password, password):
        error = "Zle haslo"

    if error is not None:
        flash(error)

    session.clear()
    session["user-id"] = user.id
    return redirect(url_for("views.user"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("views.user"))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user-id")
    if user_id is None:
        g.user = None
        g.admin = False
    else:
        g.user = User.query.filter_by(id=user_id).first()
        if g.user and g.user.admin:
            g.admin = True
        else:
            g.admin = False


@bp.before_app_request
def load_collection_and_config():
    rows = list(db.session.query(Config).all())
    g.config = {row.name: row.value for row in rows}
    g.config_description = {row.name: row.description for row in rows}


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.admin:
            return redirect(url_for("views.user"))
        return view(**kwargs)

    return wrapped_view
