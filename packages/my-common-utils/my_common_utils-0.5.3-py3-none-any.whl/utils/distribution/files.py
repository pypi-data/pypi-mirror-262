import os

from utils.config import ROOT_DIR, get_root_dir
from utils.logger import create_logger


log = create_logger("Distribution Utils")


def print_root_dir(dunder_file=None):
    if dunder_file:
        root_dir = get_root_dir(dunder_file)
    else:
        root_dir = ROOT_DIR
    log.info(f"Root dir: {root_dir} - Files in root dir: {os.listdir(root_dir)}")
