import os
import subprocess


def compile(filepath):
    """
    Compile mdx file to Javascript and return content as string.
    """
    args = [
        os.path.abspath("assets/qjs.exe"),
        "--module",
        os.path.abspath("assets/mdxcompiler.js"),
        os.path.abspath(filepath),
    ]
    p = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        shell=False,
        encoding="UTF-8",
        close_fds=False,
    )
    p.wait()
    content = p.stdout.read()
    return content
