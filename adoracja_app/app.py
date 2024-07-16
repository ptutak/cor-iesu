import os.path
from pathlib import Path

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import load_config
from .const import ConfigKeys

database = SQLAlchemy()

ROOT_CONFIG_PATH = Path(__file__).parent


def create_app(root_path: Path = ROOT_CONFIG_PATH):
    app = Flask(__name__)
    app.config[ConfigKeys.ROOT_PATH] = root_path

    if app.config[ConfigKeys.ENV] == "development":
        app.config[ConfigKeys.CONFIG_FILE] = root_path / "config" / "dev-config.ini"
    else:
        app.config[ConfigKeys.CONFIG_FILE] = root_path / "config" / "prod-config.ini"

    load_config(app)
    database.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, database)

    # app.register_blueprint(adoracja.auth.bp)
    # app.register_blueprint(adoracja.routes.root)
    # app.register_blueprint(adoracja.views.api)
    # app.register_blueprint(adoracja.commands.cli)

    return app
