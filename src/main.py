import logging


from .util import install_pkg
from .access_point import install

logging.basicConfig(level=logging.DEBUG)

def main():
    install_pkg("lol1", service="pip")

    breakpoint()