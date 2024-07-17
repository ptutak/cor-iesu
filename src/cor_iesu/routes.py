from flask import Blueprint, current_app, send_from_directory

root = Blueprint("root", __name__)


@root.route("/favicon.ico")
def favicon():
    return send_from_directory(current_app.root_path, "favicon.ico", mimetype="image/vnd.microsoft.icon")
