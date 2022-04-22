import logging
import os
import traceback as tb
import subprocess as sp

def resolve(path: str) -> str:
    """Resolves relative paths into absolute paths based on caller's location"""
    stack = tb.extract_stack()
    dirname = os.path.dirname(stack[-2].filename)
    return os.path.abspath(os.path.join(dirname, path))

def assert_cwd(expected_abs_path: str) -> None:
    """Asserts the current working directory"""
    cwd: str = sp.run("pwd", stdout=sp.PIPE).stdout.decode("utf-8").strip()

    assert cwd == expected_abs_path, (
        f"Working directory is not the expected {expected_abs_path}"
    )

def validate_cmd(process: sp.CompletedProcess[bytes], error_msg: str) -> None:
    """Asserts a finished command completed successfully"""
    try:
        assert process.returncode == 0
    except AssertionError as err:
        logging.exception(error_msg)
        raise err


def install_pkg(pkg_name: str, *args):
    """Installs a system package using apt-get"""
    install_cmd = sp.run(["sudo", "apt-get", "install", pkg_name, *args])
    validate_cmd(install_cmd, f"Error when installing {pkg_name}")