import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.json"


def load_config():
    with CONFIG_PATH.open("r") as f:
        return json.load(f)


def project_path(relative_path):
    return ROOT / relative_path