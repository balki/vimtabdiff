#!/usr/bin/python3

import os,sys
import argparse
import pathlib
import itertools
import tempfile
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description="Show diff in vim tab pages")
    parser.add_argument("pathA")
    parser.add_argument("pathB")
    return parser.parse_args()

def get_dir_info(dirname):
    if not dirname:
        return [],[]
    dirs, files = [], []
    dirp = pathlib.Path(dirname)
    for p in dirp.iterdir():
        if p.is_dir():
            dirs.append(p)
        else:
            files.append(p)
    return dirs, files

def get_pairs(aItems, bItems):
    aItems = [(item, 'A') for item in aItems]
    bItems = [(item, 'B') for item in bItems]
    abItems = aItems + bItems
    abItems.sort(key= lambda item: (item[0].name, item[1]))
    for _, items in itertools.groupby(abItems, lambda item: item[0].name):
        items = list(items)
        if len(items) == 2:
            (aItem, _), (bItem, _) = items
            yield aItem, bItem
        else:
            (item, tag), = items
            if tag == 'A':
                yield item, None
            else:
                yield None, item

def get_file_pairs(a, b):
    aDirs, aFiles = get_dir_info(a)
    bDirs, bFiles = get_dir_info(b)
    yield from get_pairs(aFiles, bFiles)
    for aDir, bDir in get_pairs(aDirs, bDirs):
        yield from get_file_pairs(aDir, bDir)

def main():
    args = parse_args()
    print("Helloworld")
    vimCmdFile = tempfile.NamedTemporaryFile(mode='w', delete=False)
    with vimCmdFile:
        for a, b in get_file_pairs(args.pathA, args.pathB):
            aPath = str(a) if a else "/dev/null"
            bPath = str(b) if b else "/dev/null"
            print(f"tabedit {aPath} | diffthis | vsp {bPath} | diffthis", file=vimCmdFile)
        print(f"""call delete("{vimCmdFile.name}")""", file=vimCmdFile)
    subprocess.run(["vim", "-S", vimCmdFile.name])

if __name__ == '__main__':
    main()

