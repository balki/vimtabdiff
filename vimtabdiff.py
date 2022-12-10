#!/usr/bin/python3

import os
import argparse
import pathlib
import itertools
import tempfile
import subprocess


def star(f):
    """ see https://stackoverflow.com/q/21892989 """
    return lambda args: f(*args)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Show diff of files from two directories in vim tabs")
    parser.add_argument("pathA")
    parser.add_argument("pathB")
    parser.add_argument("--vim", help="vim command to run", default="vim")
    return parser.parse_args()


def get_dir_info(dirname):
    if not dirname:
        return [], []
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
    abItems.sort(key=star(lambda item, tag: (item.name, tag)))
    for _, items in itertools.groupby(abItems,
                                      key=star(lambda item, _: item.name)):
        items = list(items)
        # NOTE: python 3.10's match expression can make this better
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
    vimCmdFile = tempfile.NamedTemporaryFile(mode='w', delete=False)
    with vimCmdFile:
        for a, b in get_file_pairs(args.pathA, args.pathB):
            aPath = a.resolve() if a else os.devnull
            bPath = b.resolve() if b else os.devnull
            print(
                f"tabedit {aPath} | diffthis | vsp {bPath} | diffthis | diffupdate",
                file=vimCmdFile)
        cmds = f"""
        tabfirst | tabclose
        call delete("{vimCmdFile.name}")
        """
        print(cmds, file=vimCmdFile)
    subprocess.run(args.vim.split() + ["-S", vimCmdFile.name])


if __name__ == '__main__':
    main()
