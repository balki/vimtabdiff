#!/usr/bin/python3

import os,sys
import argparse
import pathlib
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Show diff in vim tab pages")
    parser.add_argument("pathA")
    parser.add_argument("pathB")
    return parser.parse_args()

def get_dir_info(dirname: Path):
    if not dirname:
        return [],[]
    dirs, files = [], []
    for p in dirname.iterdir():
        if p.is_dir():
            dirs.append(p)
        else:
            files.append(p)
    return dirs, files

def get_file_pairs(a, b):
    aDirs, aFiles = get_dir_info(a)
    bDirs, bFiles = get_dir_info(b)
    pass

def main():
    dirs, files = get_dir_info(Path('.'))
    print(f"{dirs=} {files=}")
    args = parse_args()
    print("Helloworld")
    print(f"{args.pathA=} {args.pathB=}")

if __name__ == '__main__':
    main()
