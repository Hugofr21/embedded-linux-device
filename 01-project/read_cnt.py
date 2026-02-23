"""
read_myproc.py: demonstrates reading /proc/myproc from
a program in user space.
"""

import os

PROC_PATH = "/proc/myproc"

def read_proc():
    if not os.path.exists(PROC_PATH):
        raise FileNotFoundError(f"{PROC_PATH} It doesn't exist. Is the module loaded?")
    with open(PROC_PATH, "r") as f:
        return f.read()

if __name__ == "__main__":
    try:
        data = read_proc()
        print(f"Content of {PROC_PATH}:\n{data}")
    except Exception as exc:
        print(f"Erro: {exc}")
