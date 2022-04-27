import logging
import os
import subprocess as sp
import shutil
import sys


from . import util
from .access_point import install
from .config import config

logging.basicConfig(level=logging.DEBUG)

def main():
    if os.geteuid() == 0:
        print("We're root!")
    else:
        print("We're not root.")
        sp.call(['sudo', 'python3', *sys.argv])
        sys.exit()

    # Install dependencies
    util.install_pkg("python3-pip", service="apt-get", sudo=True)
    util.install_pkg("nginx", service="apt-get", sudo=True)
    util.install_pkg("flask", service="pip", sudo=True)
    util.install_pkg("uwsgi", service="pip", sudo=True)

    # Server directory setup
    path = config.web_server.directory

    os.chdir(path.expanduser().parent)
    os.mkdir(path.name)
    util.sudo(f"chown www-data {path.name}")
    os.chdir(path.expanduser())

    # uWSGI setup
    with open(util.resolve_relative("../files/uwsgi.ini"), "r+") as file:
        contents = file.read()

        contents = contents.replace(
            "chdir = /home/pi/flasktest",
            f"chdir = {path.expanduser()}"
        )

        contents = contents.replace(
            "flasktest.sock",
            f"{path.name}.sock"
        )

        file.seek(0)
        file.write(contents)
        file.truncate()

    util.sudo(f"cp {util.resolve_relative('../files/app.py')} app.py")
    util.sudo(f"cp {util.resolve_relative('../files/uwsgi.ini')} uwsgi.ini")

    # NGINX Setup
    shutil.copy(
        util.resolve_relative("../files/server_proxy_init"),
        util.resolve_relative("../files/server_proxy")
    )

    with open(util.resolve_relative("../files/server_proxy"), "r+") as file:
        contents = file.read()

        contents = contents.replace(
            "/tmp/flasktest.sock;",
            f"/tmp/{path.name}.sock"
        )

        file.seek(0)
        file.write(contents)
        file.truncate()

    util.sudo("rm /etc/nginx/sites-enabled/default")
    util.sudo(f"mv {util.resolve_relative('../files/server_proxy')} /etc/nginx/sites-available/{path.name}_proxy")
    util.sudo(f"ln -s /etc/nginx/sites-available/{path.name}_proxy /etc/nginx/sites-enabled")
    util.sudo("systemctl restart nginx")

    # Run uWSGI when the Pi boots

    shutil.copy(
        util.resolve_relative("../files/uwsgi.service_init"),
        util.resolve_relative("../files/uwsgi.service")
    )

    with open(util.resolve_relative("../files/uwsgi.service"), "r+") as file:
        contents = file.read()

        contents = contents.replace(
            "/home/pi/flasktest",
            f"{path.expanduser()}"
        )

        file.seek(0)
        file.write(contents)
        file.truncate()

    util.sudo(f"mv {util.resolve_relative('../files/uwsgi.service')} /etc/systemd/system/uwsgi.service")
    util.sudo("systemctl daemon-reload")
    util.sudo("systemctl start uwsgi.service")
    util.sudo("systemctl enable uwsgi.service")


















    breakpoint()