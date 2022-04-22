import os
import traceback as tb
import subprocess as sp

def resolve(path: str) -> str:
    """Resolves relative paths into absolute paths based on caller's location"""
    stack = tb.extract_stack()
    dirname = os.path.dirname(stack[-2].filename)
    return os.path.abspath(os.path.join(dirname, path))

def assert_cwd(path: str) -> None:
    """Asserts the current working directory, raising an exception if not correct"""
    cwd: str = sp.run("pwd", stdout=sp.PIPE).stdout.decode("utf-8").strip()
    expected_cwd: str = util.resolve(path)

    assert cwd == expected_cwd, f"Working directory is not the expected {expected_cwd}"