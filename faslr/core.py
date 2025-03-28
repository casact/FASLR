import configparser
import os
from faslr.constants import CONFIG_PATH


def get_startup_db_path(
        config_path: str = CONFIG_PATH
) -> str:
    """
    Extracts the db path when the user opts to connect to one automatically upon startup.
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    config.sections()
    startup_db = config['STARTUP_CONNECTION']['startup_db']

    return startup_db


config_path: str = CONFIG_PATH

use_sample = False

# Flag to determine whether there is an active database connection. Most project-related functions
# should be disabled unless a connection is established.
connection_established = False
db = None


# If a startup db has been indicated, get the path.
if os.path.isfile(config_path):
    startup_db: str = get_startup_db_path(config_path=config_path)
    if (startup_db is not None) and (not use_sample) and (startup_db != "None"):
        db = startup_db
    else:
        startup_db: None = None
else:
    startup_db: None = None

def set_db(path: str) -> None:
    global db
    db = path


