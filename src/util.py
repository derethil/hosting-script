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