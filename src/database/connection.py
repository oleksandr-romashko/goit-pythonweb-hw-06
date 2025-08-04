"""
Database connection configuration module.

This module reads database connection settings from `config.ini`
and constructs a SQLAlchemy-compatible database URL and engine.
"""

import sys
import configparser
from pathlib import Path

from sqlalchemy import create_engine

# Read database configuration from config file
db_config_file = Path(__file__).parent.parent.parent.joinpath("config.ini").resolve()
config = configparser.ConfigParser()
if not db_config_file.exists():
    sys.exit(
        f"❌ Missing configuration file: {db_config_file}\n"
        "Please copy 'config.ini.example' to 'config.ini' and update the values."
    )
config.read(db_config_file)

if "DB" not in config:
    sys.exit(
        f"❌ Missing [DB] section in {db_config_file}\n"
        "Please ensure it has the following format:\n\n"
        "[DB]\nUSER=your_user\nPASSWORD=your_password\nHOST=localhost\nPORT=5432\nDB_NAME=your_db\n"
    )

try:
    db_user = config.get("DB", "USER")
    db_password = config.get("DB", "PASSWORD")
    db_host = config.get("DB", "HOST")
    db_port = config.get("DB", "PORT")
    db_name = config.get("DB", "DB_NAME")
except configparser.NoOptionError as e:
    sys.exit(f"❌ Missing required option in [DB] section: {e}")
# db_user = config.get("DB", "user")
# db_password = config.get("DB", "password")
# db_host = config.get("DB", "host")
# db_port = config.get("DB", "port")
# db_name = config.get("DB", "db_name")

url_to_db = (
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

engine = create_engine(url_to_db, echo=True)
