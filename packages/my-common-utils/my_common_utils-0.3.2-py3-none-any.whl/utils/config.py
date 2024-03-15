import yaml
import dotenv
import os
from os import getenv as secret  # noqa: F401

from src.utils.logger import create_logger


logger = create_logger("Config Helper")

# check if venv is in the path, if not, use None as root dir
try:
    ROOT_DIR = os.path.abspath(__file__).split("venv")[0]
except Exception as e:
    logger.warn("Could not find venv in path. Using None as ROOT_DIR")
    ROOT_DIR = None

dotenv.load_dotenv()  # load .env file to be imported

try:
    stream = open(f"{ROOT_DIR}config.yml", "r", encoding="utf-8")
    config_dict = yaml.safe_load(stream)
except Exception as e:
    logger.warn(f"Could not load config.yml. This might be due to missing ROOT_DIR")
    config_dict = None


def config(key):
    return config_dict[key]
