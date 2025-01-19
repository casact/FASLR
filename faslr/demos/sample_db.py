import os
import subprocess

import faslr.core
import faslr.core as core

from faslr.constants import (
    ROOT_PATH,
    SAMPLE_DB_DEFAULT_PATH
)

def set_sample_db() -> None:
    """
    Overrides the default db to be the sample db, and not the one the user may be connected to in the config.
    """

    if os.path.exists(SAMPLE_DB_DEFAULT_PATH):
        pass
    else:
        subprocess.run(['python', ROOT_PATH + '/samples/db/generate_sample_db.py'])
    core.use_sample = True
    faslr.core.set_db(SAMPLE_DB_DEFAULT_PATH)
