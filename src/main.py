import logging
import os
import shutil

from .util import *
from . import access_point
from .config import config

logging.basicConfig(level=logging.DEBUG)

def main():
    # Install dependencies
    install_pkg("nginx", "--assume-yes", sudo=True)
    install_pkg("flask", service="pip", sudo=True)
    install_pkg("uwsgi", service="pip", sudo=True)

    print_info("installing dependencies finished")

    # Server directory setup
    path = config.web_server.directory

    os.chdir(path.expanduser().parent)
    os.mkdir(path.name)
    sudo(f"chown www-data {path.name}")
    os.chdir(path.expanduser())
    print_info("server directory created")

    # uWSGI setup

    configure_file(resolve_relative("../files/uwsgi.ini"),
        old="/home/pi/flasktest",
        new=f"{path.expanduser()}"
    )

    configure_file(resolve_relative("../files/uwsgi.ini"),
        old="flasktest.sock",
        new=f"{path.name}.sock"
    )

    sudo(f"cp {resolve_relative('../files/app.py')} app.py")
    sudo(f"cp {resolve_relative('../files/uwsgi.ini')} uwsgi.ini")

    print_info("server files setup")

    # NGINX Setup
    shutil.copy(
        resolve_relative("../files/server_proxy_init"),
        resolve_relative("../files/server_proxy")
    )

    configure_file(resolve_relative("../files/server_proxy"),
        old="/tmp/flasktest.sock;",
        new=f"/tmp/{path.name}.sock;"
    )

    print_info("reverse proxy created")

    sudo("rm /etc/nginx/sites-enabled/default")
    sudo(f"mv {resolve_relative('../files/server_proxy')} /etc/nginx/sites-available/{path.name}_proxy")
    sudo(f"ln -s /etc/nginx/sites-available/{path.name}_proxy /etc/nginx/sites-enabled")
    sudo("systemctl restart nginx")

    print_info("nginx setup complete")

    # Run uWSGI when the Pi boots

    shutil.copy(
        resolve_relative("../files/uwsgi.service_init"),
        resolve_relative("../files/uwsgi.service")
    )

    configure_file(resolve_relative("../files/uwsgi.service"),
        old="/home/pi/flasktest",
        new=f"{path.expanduser()}"
    )

    sudo(f"mv {resolve_relative('../files/uwsgi.service')} /etc/systemd/system/uwsgi.service")
    sudo("systemctl daemon-reload")
    sudo("systemctl start uwsgi.service")
    sudo("systemctl enable uwsgi.service")

    print_info("uwsgi setup complete")

    access_point.install()

    print_info("Script complete!")