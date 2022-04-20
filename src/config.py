# This file handles the pi-ap script setup and execution.
# https://github.com/f1linux/pi-ap

import os
from typing import Any

import yaml
from pydantic import BaseModel

import util


CONFIG_FILE = util.resolve("../config.yaml")


class AccessPointConfig(BaseModel):
    ssid: str = "RPI-AP1"
    passwd: str = "cH4nG3M3"
    ipv4subnet: str = "192.168.0.1/28"


class Config(BaseModel):
    access_point: AccessPointConfig()

    def load_file(self, path) -> "Config":
        with open(path) as f:
            contents = f.read()

        return self.parse_obj(yaml.load(contents, Loader=yaml.CLoader))


if os.path.isfile(CONFIG_FILE):
    config: Config = Config.load_file(Config, CONFIG_FILE)
else:
    config = Config()

print(config.access_point.ssid)