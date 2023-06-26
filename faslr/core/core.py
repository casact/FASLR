from faslr.connection import get_startup_db_path


class FCore:
    def __init__(self):

        # If a startup db has been indicated, get the path.
        self.startup_db = get_startup_db_path()

        # Flag to determine whether there is an active database connection. Most project-related functions
        # should be disabled unless a connection is established.
        self.connection_established = False
        self.db = None

    def set_db(self, path: str) -> None:

        self.db = path
