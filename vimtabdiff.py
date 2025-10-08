#!/usr/bin/python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import argparse
import itertools
import tempfile
import subprocess
import shlex
from pathlib import Path
from typing import TypeVar
from collections.abc import Iterator, Callable

R = TypeVar('R')


def star(f: Callable[..., R]) -> Callable[[tuple], R]:
    """ see https://stackoverflow.com/q/21892989 """
    return lambda args: f(*args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Show diff of files from two directories in vim tabs",
        epilog="See https://github.com/balki/vimtabdiff for more info")
    parser.add_argument("pathA", type=Path)
    parser.add_argument("pathB", type=Path)
    parser.add_argument("pathC", type=Path, nargs='?')
    parser.add_argument("--vim", help="vim command to run", default="vim")
    parser.add_argument(
        "--onlydiffs", help="only open files where there is a diff", action="store_true"
    )
    parser.add_argument(
        "--skipmissing", help="skip non-existent files", action="store_true"
    )
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


def get_triplets(
        aPaths: list[Path],
        bPaths: list[Path],
        cPaths: list[Path]) -> Iterator[tuple[
            Path | None,
            Path | None,
            Path | None]]:
    aItems = [(item, 'A') for item in aPaths]
    bItems = [(item, 'B') for item in bPaths]
    cItems = [(item, 'C') for item in cPaths]
    abcItems = aItems + bItems + cItems
    abcItems.sort(key=star(lambda item, tag: (item.name, tag)))
    for _, items in itertools.groupby(abcItems,
                                      key=star(lambda item, _: item.name)):
        match list(items):
            case [(aItem, _), (bItem, _), (cItem, _)]:
                yield aItem, bItem, cItem
            case [(aItem, 'A'), (bItem, 'B')]:
                yield aItem, bItem, None
            case [(aItem, 'A'), (cItem, 'C')]:
                yield aItem, None, cItem
            case [(bItem, 'B'), (cItem, 'C')]:
                yield None, bItem, cItem
            case [(item, 'A')]:
                yield item, None, None
            case [(item, 'B')]:
                yield None, item, None
            case [(item, 'C')]:
                yield None, None, item


def get_file_triplets(
        a: Path | None,
        b: Path | None,
        c: Path | None) -> Iterator[tuple[
            Path | None, Path | None, Path | None]]:
    aDirs, aFiles = get_dir_info(a)
    bDirs, bFiles = get_dir_info(b)
    cDirs, cFiles = get_dir_info(c)
    yield from get_triplets(aFiles, bFiles, cFiles)
    for aDir, bDir, cDir in get_triplets(aDirs, bDirs, cDirs):
        yield from get_file_triplets(aDir, bDir, cDir)


def main() -> None:
    args = parse_args()
    vimCmdFile = tempfile.NamedTemporaryFile(mode='w', delete=False)
    with vimCmdFile:
        cmds = f"""
        let s:spr = &splitright
        set splitright
        """
        print(cmds, file=vimCmdFile)
        for a, b, c in get_file_triplets(args.pathA, args.pathB, args.pathC):
            aPath = a.resolve() if a else os.devnull
            bPath = b.resolve() if b else os.devnull
            cPath = c.resolve() if c else os.devnull
            if args.skipmissing and (not a or not b or (args.pathC and not c)):
                continue
            if args.onlydiffs and a and b:
                aContents = open(aPath, mode="rb").read()
                if aContents == open(bPath, mode="rb").read():
                    if args.pathC is None:
                        continue
                    if aContents == open(cPath, mode="rb").read():
                        continue
            if args.pathC is None:
                print(f"tabedit {aPath} | vsp {bPath}", file=vimCmdFile)
            else:
                print(f"tabedit {aPath} | vsp {bPath} | vsp {cPath}", file=vimCmdFile)
        cmds = f"""
        let &splitright = s:spr
        tabdo windo :1
        tabdo windo diffthis
        tabdo windo diffupdate
        tabfirst | tabclose
        call delete("{vimCmdFile.name}")
        """
        print(cmds, file=vimCmdFile)
    subprocess.run(shlex.split(args.vim) + ["-S", vimCmdFile.name])


if __name__ == '__main__':
    main()
