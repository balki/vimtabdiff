Do you use `git difftool` to review changes before making a commit? The problem with that is that you get to see the diff of one file at a time. You can't easily stop it after few files and you can't go back to a previous file. `vimtabdiff.py` loads all the files with diffs, one in each vim tab page. You can move around any file and edit the diffs easily.


# Install

    mkdir -p ~/bin

    # for python version >= 3.10
    curl -o ~/bin/vimtabdiff.py "https://raw.githubusercontent.com/balki/vimtabdiff/master/vimtabdiff.py"

    # for python version < 3.10
    curl -o ~/bin/vimtabdiff.py "https://raw.githubusercontent.com/balki/vimtabdiff/py38/vimtabdiff.py"

    chmod +x ~/bin/vimtabdiff.py

You may need to add `~/bin` to your PATH variable if not already done. See [here](needed://wiki.archlinux.org/title/Environment_variables#Per_user) for help.
👍 this [issue](https://github.com/balki/vimtabdiff/issues/1) for `pip install` support 


# Screenshot
![image](https://user-images.githubusercontent.com/189196/206880555-c71b472c-144c-4c82-a4ab-f8a4fd36f7a5.png)

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

## Relevant vim tips

  * `gt`                 → Go to next tab
  * `gT`                 → Go to previous tab
  * `:tabr`              → Go to first tab
  * `:drop filenam<Tab>` → Go to the tab with filename
  * `g<Tab>`             → Go to last used tab (Works in vim version > 8.2.1401)
  * `set mouse`          → Now clicking on a tab works
  * `]c`                 → Go to next diff hunk
  * `[c`                 → Go to previous diff hunk
  * `do`, `dp`             → Diff obtain, Diff put
  * `zo`, `zc`, `zR`         → Fold open, Fold close, open all folds

# See Git diffs


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

  1. If your path to vim has a space, it does not work, i.e. Following does **not** work

      ```bash
      git config difftool.vimtabdiff.cmd 'vimtabdiff.py --vim "/home/foo/my program files/bin/vim" $LOCAL $REMOTE'
      ```
  2. Not tested in non-linux OS. Pull requests welcome if found any issues but hopefully should work fine.

# Similar

https://gist.github.com/Osse/4709787
