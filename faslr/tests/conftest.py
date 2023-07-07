import os
import pytest
import shutil

from faslr.constants import (
    CONFIG_TEMPLATES_PATH,
    DEFAULT_DIALOG_PATH,
    ROOT_PATH
)


@pytest.fixture()
def setup_config() -> str:
    """
    Use a temporary config file for the test.
    :return: str
    """

    if os.path.isfile(CONFIG_TEMPLATES_PATH):
        dest_path = os.path.dirname(ROOT_PATH) + '/faslr_test.ini'
        shutil.copy(CONFIG_TEMPLATES_PATH, dest_path)
    else:
        raise FileNotFoundError("CONFIG_PATH does not point to a valid config file.")

    yield dest_path

    # Teardown - delete test config file

    if os.path.isfile(dest_path):
        os.remove(dest_path)


@pytest.fixture()
def sample_db() -> str:
    """
    Make a copy of the sample db, so we do not alter the original.
    The tests will use this copy as the backend db.
    :return: The path to the copy of the sample db.
    """
    db_filename = DEFAULT_DIALOG_PATH + '/sample.db'
    test_db_filename = DEFAULT_DIALOG_PATH + '/sample_test.db'
    shutil.copy(db_filename, test_db_filename)
    yield test_db_filename

    os.remove(test_db_filename)
