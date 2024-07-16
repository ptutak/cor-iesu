import configparser
from pathlib import Path
from urllib.parse import quote_plus

from flask import Flask

from .const import ConfigKeys


class InvalidConfig(Exception):
    """
    Raised in case of missing config section or value
    """


def load_config(app: Flask):
    config_file = app.config[ConfigKeys.CONFIG_FILE]
    config = configparser.ConfigParser()
    config.read(config_file)

    VALID_KEYS = {
        "app": {"secret_key"},
        "database": {"username", "password", "name", "address"},
        "database-dev": {"path"},
    }

    MANDATORY_SECTIONS = {"app", "database"}

    config_keys = set(config.keys())
    if not MANDATORY_SECTIONS <= config_keys:
        missing_sections = MANDATORY_SECTIONS - config_keys
        raise InvalidConfig(f"Mandatory sections missing: {missing_sections}")

    for key in config_keys:
        if key not in VALID_KEYS:
            continue
        config_values = set(config[key].keys())
        valid_values = VALID_KEYS[key]
        if valid_values != config_values:
            raise InvalidConfig(f"Valid config values for section: {key}, are: {valid_values}")

    app.secret_key = config["app"]["secret_key"]

    if app.config[ConfigKeys.ENV] == "development":
        path = Path(app.config[ConfigKeys.ROOT_PATH]) / config["database-dev"]["path"]
        app.config[ConfigKeys.SQLALCHEMY_DATABASE_URI] = f"sqlite:///{path.absolute()}"
    else:
        address = config["database"]["address"]
        username = config["database"]["username"]
        password = config["database"]["password"]
        password = quote_plus(password)
        name = config["database"]["name"]
        app.config[ConfigKeys.SQLALCHEMY_DATABASE_URI] = f"mysql://{username}:{password}@{address}/{name}"
