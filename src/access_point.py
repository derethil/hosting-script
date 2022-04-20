# This file handles the pi-ap script setup and execution.
# https://github.com/f1linux/pi-ap

import logging
import os
import re
import subprocess as sp

from . import util
from .config import config

PI_AP_URL = "https://github.com/f1linux/pi-ap"

def assert_cwd(path: str) -> None:
    """Asserts the current working directory, raising an exception if not correct"""
    cwd: str = sp.run("pwd", stdout=sp.PIPE).stdout.decode("utf-8").strip()
    expected_cwd: str = util.resolve(path)

    assert cwd == expected_cwd, f"Working directory is not the expected {expected_cwd}"


def replace(key: str, value: str) -> None:
    """Replaces a single pi-ap config option"""
    assert_cwd("../pi-ap/")

    PI_AP_CONFIG = "./variables.sh"

    with open(PI_AP_CONFIG, "r+") as file:
        contents = file.read()
        new_contents = re.sub(f"{key}='.*'", f"{key}='{value}'", contents, count=1)
        file.seek(0)
        file.write(new_contents)
        file.truncate()
        logging.debug(f"Replaced {key}='{value}' with {key}='{value}'")


def set_variables():
    """Sets pi-ap's variables to config values"""
    assert_cwd("../pi-ap/")

    CONFIG_KEY = "access_point"
    config_dict: dict[str, str] = config.dict()[CONFIG_KEY]

    for key, value in config_dict.items():
        replace(key.upper(), value)


# Setup

def install():
    os.chdir(util.resolve("../"))
    logging.debug(f"Cloning {PI_AP_URL}")
    git_clone_cmd = sp.run(["git", "clone", PI_AP_URL])

    try:
        assert git_clone_cmd.returncode == 0
    except AssertionError as err:
        logging.exception("Something went wrong cloning the pi-ap repository")
        raise err

    os.chdir(util.resolve("../pi-ap/"))
    set_variables()

    logging.debug("Installing pi-ap from ./install.sh")
    install_cmd = sp.run("pwd")

    try:
        assert install_cmd.returncode == 0
    except AssertionError as err:
        logging.exception("Something went wrong installing pi-ap")
        raise err

    os.chdir(util.resolve("../"))

    logging.debug("Removing pi-ap/ directory")
    sp.run(["rm", "-rf", "pi-ap/"])

