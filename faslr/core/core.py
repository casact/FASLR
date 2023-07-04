import os
from faslr.connection import get_startup_db_path
from faslr.constants import CONFIG_PATH


class FCore:
    def __init__(
            self,
            config_path: str = CONFIG_PATH
    ):

        # If a startup db has been indicated, get the path.
        if os.path.isfile(config_path):
            self.startup_db = get_startup_db_path(config_path=config_path)
        else:
            self.startup_db = None

        # Flag to determine whether there is an active database connection. Most project-related functions
        # should be disabled unless a connection is established.
        self.connection_established = False
        self.db = None

    def set_db(self, path: str) -> None:

        self.db = path
