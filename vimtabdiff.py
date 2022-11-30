#!/usr/bin/python3

import os,sys

def main():
    local, remote = sys.argv[1:]
    print("Helloworld")
    print(f"{local=} {remote=}")

if __name__ == '__main__':
    main()
