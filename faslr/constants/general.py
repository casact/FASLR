import git
import os

from faslr._version import __version__
from os.path import dirname
from PyQt6.QtWidgets import QFileDialog


BUILD_VERSION = __version__

# if "PYCHARM_HOSTED" in os.environ:
#     QT_FILEPATH_OPTION = QFileDialog.Option.DontUseNativeDialog
# # Don't cover this, can't test without leaving PyCharm.
# else:  # pragma no coverage
#     QT_FILEPATH_OPTION = QFileDialog.Option.ShowDirsOnly

QT_FILEPATH_OPTION = QFileDialog.Option.DontUseNativeDialog

# Path of the main faslr code moduels (e.g., FASLR/faslr)
ROOT_PATH = dirname(dirname(os.path.realpath(__file__)))

# Path of the FASLR main repo (e.g., FASLR)
REPO_PATH = dirname(ROOT_PATH)

# Path of the configuration file
CONFIG_PATH = os.path.join(ROOT_PATH, 'faslr.ini')

# Path for template files, i.e., the generic configuration file
TEMPLATES_PATH = os.path.join(dirname(dirname(os.path.realpath(__file__))), 'templates')

CONFIG_TEMPLATES_PATH = os.path.join(TEMPLATES_PATH, 'config_template.ini')

# Default path for file saves and opens

DEFAULT_DIALOG_PATH = dirname(ROOT_PATH)

SAMPLE_DIALOG_PATH = dirname(ROOT_PATH) + '/faslr/samples/'

# Path for icons
ICONS_PATH = os.path.join(dirname(dirname(os.path.realpath(__file__))), 'style/icons/')

# URL of the documentation website
DOCUMENTATION_URL = 'https://faslr.com'

GITHUB_URL = 'https://github.com/casact/faslr'

DISCUSSIONS_URL = 'https://github.com/casact/FASLR/discussions'

ISSUES_URL = 'https://github.com/casact/FASLR/issues'

OCTICONS_PATH = os.path.join(
    dirname(dirname(os.path.realpath(__file__))),
    'style/icons/octicons/'
)


repo = git.Repo(search_parent_directories=True)

try:
    branch = repo.active_branch
    CURRENT_BRANCH = branch.name
    BRANCH_SHA = repo.git.rev_parse(
        branch,
        short=6
    )
# Don't cover this block - won't be able to test it without leaving current commit
except TypeError:  # pragma no coverage
    CURRENT_BRANCH = "Detached HEAD"
    BRANCH_SHA = "None"

sha = repo.head.commit.hexsha

CURRENT_COMMIT_LONG = sha

CURRENT_COMMIT = repo.git.rev_parse(
    sha,
    short=6
)

SAMPLE_DB_NAME = 'sample.db'

SAMPLE_DB_DEFAULT_PATH = REPO_PATH + '/' + SAMPLE_DB_NAME