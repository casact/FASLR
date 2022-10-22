import os
from os.path import dirname
from PyQt6.QtWidgets import QFileDialog

BUILD_VERSION = "0.0.2"

if "PYCHARM_HOSTED" in os.environ:
    QT_FILEPATH_OPTION = QFileDialog.Option.DontUseNativeDialog
else:
    QT_FILEPATH_OPTION = QFileDialog.Option.ShowDirsOnly


ROOT_PATH = dirname(dirname(os.path.realpath(__file__)))

CONFIG_PATH = os.path.join(ROOT_PATH, 'faslr.ini')

TEMPLATES_PATH = os.path.join(dirname(dirname(os.path.realpath(__file__))), 'templates')

ICONS_PATH = os.path.join(dirname(dirname(os.path.realpath(__file__))), 'style/icons/')
