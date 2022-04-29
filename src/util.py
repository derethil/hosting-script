import logging
import os
import traceback as tb
import subprocess as sp
import print_color
def resolve_relative(path: str) -> str:
    """Resolves relative paths into absolute paths based on caller's location"""
    stack = tb.extract_stack()
    dirname = os.path.dirname(stack[-2].filename)
    return os.path.abspath(os.path.join(dirname, path))

def resolve_home(path: str) -> str:
    """Expands paths containing ~/ character"""
    return os.path.abspath(os.path.expanduser(path))

def assert_cwd(expected_abs_path: str) -> None:
    """Asserts the current working directory"""
    cwd: str = sp.run("pwd", stdout=sp.PIPE).stdout.decode("utf-8").strip()

    assert cwd == expected_abs_path, (
        f"Working directory is not the expected {expected_abs_path}"
    )

def sudo(cmd: str) -> sp.CompletedProcess:
    args = cmd.split(" ")
    return sp.run(["sudo", *args])

def validate_cmd(process: sp.CompletedProcess[bytes], error_msg: str = None) -> None:
    """Asserts a finished command completed successfully"""
    if error_msg is None:
        error_msg = f"Error on running command: {' '.join(process.args)}"

    try:
        assert process.returncode == 0
    except AssertionError as err:
        logging.exception(error_msg)
        raise err


def install_pkg(pkg_name: str, *args, service: str = "apt-get", sudo: bool = False):
    """Installs a system package. Uses apt-get by default."""
    arg_list = [service, "install", pkg_name, *args]
    install_cmd = sp.run(["sudo", *arg_list] if sudo else [*arg_list])
    validate_cmd(install_cmd)

def print_info(msg: str):
    print()
    print_color.print(f"{msg}", tag="info", tag_color="green", format="bold", color="white")
    print()

def configure_file(path: str, *, old: str, new: str) -> None:
    with open(path, "r+") as file:
        contents = file.read()

        contents = contents.replace(old, new)

        file.seek(0)
        file.write(contents)
        file.truncate()