import logging
import os
import subprocess as sp


from . import util
from .access_point import install
from .config import config

logging.basicConfig(level=logging.DEBUG)

def main():
    # Install dependencies
    util.install_pkg("nginx", service="apt-get", sudo=True)
    util.install_pkg("flask", service="pip", sudo=True)
    util.install_pkg("uwsgi", service="pip", sudo=True)

    # Flask setup
    path = config.web_server.directory

    os.chdir(path.expanduser().parent)
    os.mkdir(path.name)
    sp.run(["sudo", "chown", "www-data", path.name])
    os.chdir(path)







    breakpoint()