import git
import os
from os.path import dirname
from PyQt6.QtWidgets import QFileDialog


BUILD_VERSION = "0.0.4"

if "PYCHARM_HOSTED" in os.environ:
    QT_FILEPATH_OPTION = QFileDialog.Option.DontUseNativeDialog
else:
    QT_FILEPATH_OPTION = QFileDialog.Option.ShowDirsOnly


ROOT_PATH = dirname(dirname(os.path.realpath(__file__)))

CONFIG_PATH = os.path.join(ROOT_PATH, 'faslr.ini')

TEMPLATES_PATH = os.path.join(dirname(dirname(os.path.realpath(__file__))), 'templates')

ICONS_PATH = os.path.join(dirname(dirname(os.path.realpath(__file__))), 'style/icons/')

DOCUMENTATION_URL = 'https://faslr.com'

GITHUB_URL = 'https://github.com/casact/faslr'

DISCUSSIONS_URL = 'https://github.com/casact/FASLR/discussions'

ISSUES_URL = 'https://github.com/casact/FASLR/issues'

OCTICONS_PATH = os.path.join(dirname(dirname(os.path.realpath(__file__))), 'style/icons/octicons/')


repo = git.Repo(search_parent_directories=True)

branch = repo.active_branch

CURRENT_BRANCH = branch.name

sha = repo.head.commit.hexsha

CURRENT_COMMIT = repo.git.rev_parse(
    sha,
    short=6
)

BRANCH_SHA = repo.git.rev_parse(
    branch,
    short=6
)