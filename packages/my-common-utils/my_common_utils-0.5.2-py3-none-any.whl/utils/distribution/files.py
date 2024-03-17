import os

from utils.config import ROOT_DIR
from utils.logger import create_logger


log = create_logger("Distribution Utils")


def print_root_dir(root_dir: str | None = None):
    if root_dir is None:
        root_dir = ROOT_DIR
    log.info(f"Root dir: {root_dir} - Files in root dir: {os.listdir(root_dir)}")
