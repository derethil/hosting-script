import os
import traceback as tb

def resolve(path: str) -> str:
    stack = tb.extract_stack()
    dirname = os.path.dirname(stack[-2].filename)
    return os.path.abspath(os.path.join(dirname, path))