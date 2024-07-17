import os
from pathlib import Path

from flask import Flask
from flask_migrate import Migrate


from .config import load_config
from .const import ConfigKeys


ROOT_CONFIG_PATH = Path(__file__).parent


def create_app(root_path: os.PathLike[str] | None = None) -> Flask:
    app = Flask(__name__)
    app.config[ConfigKeys.ROOT_PATH] = ROOT_CONFIG_PATH

    if ConfigKeys.ENV not in app.config:
        app.config[ConfigKeys.ENV] = "development"

    if root_path is None:
        if app.config[ConfigKeys.ENV] == "development":
            root_path = ROOT_CONFIG_PATH / "config" / "dev-config.ini"
        else:
            root_path = ROOT_CONFIG_PATH / "config" / "prod-config.ini"

    app.config[ConfigKeys.CONFIG_FILE] = root_path

    load_config(app)

    import cor_iesu.models

    database = cor_iesu.models.db
    database.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, database)

    import cor_iesu.auth
    import cor_iesu.routes
    import cor_iesu.views

    app.register_blueprint(cor_iesu.auth.bp)
    app.register_blueprint(cor_iesu.routes.root)
    app.register_blueprint(cor_iesu.views.api)

    with app.app_context():
        database.create_all()

    return app
