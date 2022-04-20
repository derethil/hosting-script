


import os

import yaml
from pydantic import BaseModel

import util


CONFIG_FILE = util.resolve("../config.yaml")


class AccessPointConfig(BaseModel):
    ssidname: str = "RPI-AP1"
    apwpa2passwd: str = "cH4nG3M3"
    ipv4ipwlan0: str = "192.168.0.1/28"


class Config(BaseModel):
    access_point: AccessPointConfig = AccessPointConfig()

    @classmethod
    def from_file(cls, file):
        with open(file) as f:
            contents = f.read()

        data = yaml.load(contents, Loader=yaml.CLoader)
        return cls(**data)


if os.path.isfile(CONFIG_FILE):
    config: Config = Config.from_file(CONFIG_FILE)
else:
    config = Config()