import yaml
from dotenv import load_dotenv
import os
from os import getenv as secret  # noqa: F401

from utils.logger import create_logger


def get_root_dir(dunder_file):
    root_dir = None
    try:
        if not ("venv" in os.path.abspath(dunder_file) or "src" in os.path.abspath(dunder_file)):
            logger.error(f"No src or venv dir in {dunder_file}")
        else:
            root_dir = os.path.abspath(dunder_file).split("venv")[0]
            root_dir = os.path.abspath(dunder_file).split("src")[0]
    except Exception:
        logger.error(f"Could not get root dir from {dunder_file}")
    finally:
        logger.debug(f"ROOT_DIR: {root_dir}")
        return root_dir



def load_config_yaml(file_path: str):
    try:
        _stream = open(file_path, "r", encoding="utf-8")
        return yaml.safe_load(_stream)
    except Exception as e:
        logger.error(f"Could not load config from {file_path}")
        return None


def config_entry(key):
    return CONFIG[key]


logger = create_logger("Config Helper")
load_dotenv()
ROOT_DIR = get_root_dir(__file__)
CONFIG = load_config_yaml(f"{ROOT_DIR}config.yml")
