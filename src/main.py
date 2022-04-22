from asyncio import subprocess
import logging
import subprocess

from .util import install_pkg
from .access_point import install

logging.basicConfig(level=logging.DEBUG)

def main():
    install_pkg("lol1")
    # subprocess.run(["sudo", "pacman", "-Syu"])