import os
from pathlib import Path

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import load_config
from .const import ConfigKeys

database = SQLAlchemy()

ROOT_CONFIG_PATH = Path(__file__).parent


def create_app(root_path: os.PathLike[str] | None = None) -> Flask:
    app = Flask(__name__)
    app.config[ConfigKeys.ROOT_PATH] = root_path

    if ConfigKeys.ENV not in app.config:
        app.config[ConfigKeys.ENV] = "development"

    if root_path is None:
        if app.config[ConfigKeys.ENV] == "development":
            root_path = ROOT_CONFIG_PATH / "config" / "dev-config.ini"
        else:
            root_path = ROOT_CONFIG_PATH / "config" / "prod-config.ini"

    app.config[ConfigKeys.CONFIG_FILE] = root_path

    load_config(app)
    database.init_app(app)

    import cor_iesu.models

    migrate = Migrate()
    migrate.init_app(app, database)

    # app.register_blueprint(adoracja.auth.bp)
    # app.register_blueprint(adoracja.routes.root)
    # app.register_blueprint(adoracja.views.api)
    # app.register_blueprint(adoracja.commands.cli)

    return app
