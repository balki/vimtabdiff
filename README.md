# Usage
```help
    usage: vimtabdiff.py [-h] [--vim VIM] pathA pathB

    Show diff of files from two directories in vim tabs

    positional arguments:
      pathA
      pathB

    options:
      -h, --help  show this help message and exit
      --vim VIM   vim command to run
```

# Git difftool


## Setup
```bash
    git config --global difftool.vimtabdiff.cmd 'vimtabdiff.py $LOCAL $REMOTE'
    git config --global alias.dt 'difftool --tool vimtabdiff --dir-diff'
```

## Usage

```bash
    git dt <any git diff revision expression> # see `man gitrevisions`
    git dt           # Unstaged changes
    git dt --staged  # Staged changes
    git dt HEAD~1    # Last commit
    git di v1.0 v2.0 # diff between two tags
```

## Using custom vim command

```bash
    git config --global difftool.vimtabdiff.cmd 'vimtabdiff.py --vim "vim --clean" $LOCAL $REMOTE'
```

Git config file (`~/.gitconfig`) should look like this

```TOML
    [alias]
            ...
            dt = difftool --tool vimtabdiff --dir-diff
    [difftool "vimtabdiff"]
            cmd = vimtabdiff.py --vim \"vim --clean\" $LOCAL $REMOTE
```


# Known issues

  1. If your path to custom vim has space, it does not work. i.e. Following does **not** work

      ```bash
      git config --global difftool.vimtabdiff.cmd 'vimtabdiff.py --vim "/home/foo/my files/bin/vim" $LOCAL $REMOTE'
      ```
  2. Not tested in non-linux OS. Pull requests welcome if found any issues but hopefully should work fine.

# Similar

https://gist.github.com/Osse/4709787
