import os
from os.path import dirname
from PyQt5.QtWidgets import QFileDialog

BUILD_VERSION = "0.0.0"

if "PYCHARM_HOSTED" in os.environ:
    QT_FILEPATH_OPTION = QFileDialog.DontUseNativeDialog
else:
    QT_FILEPATH_OPTION = QFileDialog.ShowDirsOnly


SETTINGS_LIST = [
    "Startup",
    "User"
]

ROOT_PATH = dirname(dirname(os.path.realpath(__file__)))

CONFIG_PATH = os.path.join(ROOT_PATH, 'faslr.ini')

TEMPLATES_PATH = os.path.join(dirname(os.path.realpath(__file__)), 'templates')
