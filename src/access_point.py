# This file handles the pi-ap script setup and execution.
# https://github.com/f1linux/pi-ap

import os
import re
import subprocess as sp

import util
from config import config

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


def set_variables():
    """Sets pi-ap's variables to config values"""
    assert_cwd("../pi-ap/")

    CONFIG_KEY = "access_point"
    config_dict: dict[str, str] = config.dict()[CONFIG_KEY]

    for key, value in config_dict.items():
        replace(key.upper(), value)


# Setup

os.chdir(util.resolve("../"))
#git_clone = sp.run(["git", "clone", PI_AP_URL])
os.chdir(util.resolve("../pi-ap/"))

set_variables()
