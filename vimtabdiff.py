#!/usr/bin/python3

import os,sys
import argparse
import pathlib
import itertools
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

def get_pairs(aItems, bItems):
    aItems = [(item, 'A') for item in aItems]
    bItems = [(item, 'B') for item in bItems]
    items = sorted(aItems + bItems)
    for _, items in itertools.groupby(items, lambda item: item[0].name):
        items = list(items)
        if len(items) == 2:
            (aItem, _), (bItem, _) = items
            yield aItem, bItem
        else:
            assert(len(items) == 1)
            (item, tag), = items
            if tag == 'A':
                yield item, None
            else:
                yield None, item

def get_file_pairs(a, b):
    aDirs, aFiles = get_dir_info(Path(a))
    bDirs, bFiles = get_dir_info(Path(b))
    yield from get_pairs(aFiles, bFiles)
    for aDir, bDir in get_pairs(aDirs, bDirs):
        yield from get_file_pairs(aDir, bDir)

def main():
    args = parse_args()
    print("Helloworld")
    for a, b in get_file_pairs(args.pathA, args.pathB):
        print(f"{a=}, {b=}")

if __name__ == '__main__':
    main()

