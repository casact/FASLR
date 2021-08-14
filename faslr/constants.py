import os
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