import logging
import os
import subprocess as sp


from . import util
from .access_point import install
from .config import config

logging.basicConfig(level=logging.DEBUG)

def main():
    # Create Virtual Environment

    if config.web_server.existing_flask_app:
        os.chdir(util.resolve_home(config.web_server.flask_app_path))

    else:
        os.chdir(util.resolve_home("~/"))
        os.mkdir("WebServer")
        os.chdir("./WebServer")

    util.install_pkg("flask", service="pip")
    util.install_pkg("nginx")

    breakpoint()