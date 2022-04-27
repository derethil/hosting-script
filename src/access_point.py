# This file handles the pi-ap script setup and execution.
# https://github.com/f1linux/pi-ap

import logging
import os
import re
import subprocess as sp

from . import util
from .config import config

PI_AP_URL = "https://github.com/f1linux/pi-ap"


def set_config_option(key: str, value: str) -> None:
    """Writes a single config value to variables.sh"""
    util.assert_cwd(util.resolve_relative("../pi-ap/"))

    PI_AP_CONFIG = "./variables.sh"

    with open(PI_AP_CONFIG, "r+") as file:
        contents = file.read()
        new_contents = re.sub(f"{key}='.*'", f"{key}='{value}'", contents, count=1)
        file.seek(0)
        file.write(new_contents)
        file.truncate()
        logging.debug(f"Replaced {key}='{value}' with {key}='{value}'")


def set_config():
    """Writes to pi-ap's variables.sh to match config values"""
    util.assert_cwd(util.resolve_relative("../pi-ap/"))

    CONFIG_KEY = "access_point"
    config_dict: dict[str, str] = config.dict()[CONFIG_KEY]

    for key, value in config_dict.items():
        set_config_option(key.upper(), value)


# Setup

def install():
    """Handles the install process of pi-ap"""

    # Clone repo
    os.chdir(util.resolve_relative("../"))
    logging.debug(f"Cloning {PI_AP_URL}")
    git_clone_cmd = sp.run(["git", "clone", PI_AP_URL])

    util.validate_cmd(git_clone_cmd)
    os.chdir(util.resolve_relative("../pi-ap/"))

    # Set config
    set_config()
    util.print_info("pi-ap cloned and configured")

    # Install
    logging.debug("Installing pi-ap from ./install.sh")
    install_cmd = util.sudo("./install.sh")

    util.validate_cmd(install_cmd, "Error when installing pi-ap from ./install.sh")

    # Remove leftover directory
    os.chdir(util.resolve_relative("../"))

    logging.debug("Removing pi-ap/ directory")
    sp.run(["rm", "-rf", "pi-ap/"])

    util.print_info("pi-ap successfully executed")

