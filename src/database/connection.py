"""
Database connection configuration module.

This module reads database connection settings from `config.ini`
and constructs a SQLAlchemy-compatible database URL.
"""

import configparser
from pathlib import Path

# Read database configuration from config file
db_config_file = Path(__file__).parent.parent.parent.joinpath("config.ini").resolve()
config = configparser.ConfigParser()
config.read(db_config_file)

db_user = config.get("DB", "user")
db_password = config.get("DB", "password")
db_host = config.get("DB", "host")
db_port = config.get("DB", "port")
db_name = config.get("DB", "db_name")

url_to_db = (
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
