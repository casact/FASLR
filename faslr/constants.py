import pandas as pd
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

TEMP_LDF_LIST = pd.DataFrame(
    data=[
        [True, "All-year volume-weighted", "Volume", "9"],
        [False, "3-year volume-weighted", "Volume", "3"],
        [False, "5-year volume-weighted", "Volume", "5"],
    ],
    columns=["Selected", "Label", "Type", "Number of Years"]
)

LDF_AVERAGES = {
            # 'Geometric': 'geometric',
            # 'Medial': 'medial',
            'Regression': 'regression',
            'Straight': 'simple',
            'Volume': 'volume'
}
