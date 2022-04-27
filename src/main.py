import logging
import os
import shutil


from . import util
from . import access_point
from .config import config

logging.basicConfig(level=logging.DEBUG)

def main():
    # Install dependencies
    util.install_pkg("nginx", service="apt-get", sudo=True)
    util.install_pkg("flask", service="pip", sudo=True)
    util.install_pkg("uwsgi", service="pip", sudo=True)
    util.print_info("installing dependencies finished")

    # Server directory setup
    path = config.web_server.directory

    os.chdir(path.expanduser().parent)
    os.mkdir(path.name)
    util.sudo(f"chown www-data {path.name}")
    os.chdir(path.expanduser())
    util.print_info("server directory created")

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

    util.print_info("server files setup")

    # NGINX Setup
    shutil.copy(
        util.resolve_relative("../files/server_proxy_init"),
        util.resolve_relative("../files/server_proxy")
    )

    with open(util.resolve_relative("../files/server_proxy"), "r+") as file:
        contents = file.read()

        contents = contents.replace(
            "/tmp/flasktest.sock;",
            f"/tmp/{path.name}.sock;"
        )

        file.seek(0)
        file.write(contents)
        file.truncate()

    util.print_info("reverse proxy created")

    util.sudo("rm /etc/nginx/sites-enabled/default")
    util.sudo(f"mv {util.resolve_relative('../files/server_proxy')} /etc/nginx/sites-available/{path.name}_proxy")
    util.sudo(f"ln -s /etc/nginx/sites-available/{path.name}_proxy /etc/nginx/sites-enabled")
    util.sudo("systemctl restart nginx")

    util.print_info("nginx setup complete")

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

    util.print_info("uwsgi setup complete")

    access_point.install()

    util.print_info("Script complete!")