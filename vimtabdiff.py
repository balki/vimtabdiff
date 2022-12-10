#!/usr/bin/python3

import os
import argparse
import itertools
import tempfile
import subprocess
from pathlib import Path
from typing import Callable, TypeVar
from collections.abc import Iterator, Sequence

T = TypeVar('T')


def star(f: Callable[..., T]) -> Callable[[Sequence], T]:
    """ see https://stackoverflow.com/q/21892989 """
    return lambda args: f(*args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
            description="Show diff of files from two directories in vim tabs",
            epilog="See https://github.com/balki/vimtabdiff for more info")
    parser.add_argument("pathA", type=Path)
    parser.add_argument("pathB", type=Path)
    parser.add_argument("--vim", help="vim command to run", default="vim")
    return parser.parse_args()


def get_dir_info(dirpath: Path | None) -> tuple[list[Path], list[Path]]:
    if not dirpath:
        return [], []
    dirs, files = [], []
    for p in dirpath.iterdir():
        if p.is_dir():
            dirs.append(p)
        else:
            files.append(p)
    return dirs, files


def get_pairs(aItems: list[Path],
              bItems: list[Path]) -> Iterator[tuple[Path | None, Path | None]]:
    aItems = [(item, 'A') for item in aItems]
    bItems = [(item, 'B') for item in bItems]
    abItems = aItems + bItems
    abItems.sort(key=star(lambda item, tag: (item.name, tag)))
    for _, items in itertools.groupby(abItems,
                                      key=star(lambda item, _: item.name)):
        match list(items):
            case [(aItem, _), (bItem, _)]: 
                yield aItem, bItem
            case [(item, 'A'),]:
                yield item, None
            case [(item, 'B'),]:
                yield None, item


def get_file_pairs(a: Path,
                   b: Path) -> Iterator[tuple[Path | None, Path | None]]:
    aDirs, aFiles = get_dir_info(a)
    bDirs, bFiles = get_dir_info(b)
    yield from get_pairs(aFiles, bFiles)
    for aDir, bDir in get_pairs(aDirs, bDirs):
        yield from get_file_pairs(aDir, bDir)


def main() -> None:
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
