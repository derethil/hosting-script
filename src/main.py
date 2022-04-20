import logging

from .access_point import install

logging.basicConfig(level=logging.DEBUG)

def main():
    install()