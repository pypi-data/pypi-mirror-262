import os
from pathlib import Path

import yaml

GENAIAGENTS_CONFIG_PATH = os.environ.get("GENAIAGENTS_CONFIG_PATH")
if not GENAIAGENTS_CONFIG_PATH:
    raise FileNotFoundError(
        "Environment variable not set: `GENAIAGENTS_CONFIG_PATH`"
    )
GENAIAGENTS_CONFIG_PATH = Path(GENAIAGENTS_CONFIG_PATH)
if not GENAIAGENTS_CONFIG_PATH.is_file():
    raise FileNotFoundError(
        f"No such file or directory: `{GENAIAGENTS_CONFIG_PATH.absolute()}`"
    )


def getYamlAttribute(attrName):
    with open(GENAIAGENTS_CONFIG_PATH, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        attrValue = data.get(attrName)
        return attrValue
