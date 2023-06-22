import os
import sys

from os.path import dirname
from shutil import copyfile

faslr_path = dirname(dirname(dirname(dirname(os.path.realpath(__file__)))))
sys.path.append(faslr_path)

from faslr.constants import (
    CONFIG_PATH,
    CONFIG_TEMPLATES_PATH
)

if not os.path.exists(CONFIG_PATH):

    copyfile(
        src=CONFIG_TEMPLATES_PATH,
        dst=CONFIG_PATH
    )