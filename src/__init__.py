from pathlib import Path

import os


# - CONSTANTS - #
ROOT_PATH = Path(os.getcwd())
DATA_PATH = Path(f"{ROOT_PATH}/data")
SRC_PATH = Path(f"{ROOT_PATH}/src")
TREC_PATH = Path(f"{DATA_PATH}/trec_eval")
