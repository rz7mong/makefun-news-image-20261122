#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261122 (Python 3.13, stdlib only).

Copies the broadsheet image entry.png shipped beside this file to the
grader's output directory, as /output/entry.png (or $MAKEFUN_OUTPUT_DIR
when set, the local stand-in for /output). The copy is byte-identical by
construction, so the two grading runs always write the same bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    sys.exit(main())
