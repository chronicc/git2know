#!/usr/bin/env python3

from git import GitCmdObjectDB, Repo
from git2know import HOME, INDEXDB, SYMBOL_CLEAN, SYMBOL_DIRTY, ui
from subprocess import check_call, check_output
import cli_ui as ui
import os
import shutil


HOME = os.environ["HOME"]
INDEXDB = HOME + "/.cache/mlocate.db"
SYMBOL_UNCOMMITED = ui.UnicodeSequence(ui.darkred, "⚙", "#")
SYMBOL_UNPUSHED = ui.UnicodeSequence(ui.darkyellow, "⤊", "+")
SYMBOL_UNPULLED = ui.UnicodeSequence(ui.darkblue, "⤋", "-")


def main():
    ui.info_count(0, 2, "Creating index database")
    check_call(["updatedb", "-l0", "-U", HOME, "-o", INDEXDB])
    ui.info_count(1, 2, "Searching for git repositores")
    common_args = ["-d", INDEXDB, "-r", "^.*/.git$"]
    if shutil.which("mlocate"):
        search_cmd = ["mlocate", "-q"]
    elif shutil.which("locate"):
        search_cmd = ["locate"]
    else:
        ui.error(
            "No binary for reading the mlocate database found."
            "Please install mlocate or locate."
        )
    repo_paths = check_output(search_cmd + common_args).decode().strip().split("\n")
    ui.info("")
    ui.info_section("Repositories")
    for i, path in enumerate(repo_paths):
        repo = Repo(path, odbt=GitCmdObjectDB)

        if repo.is_dirty():
            status = SYMBOL_DIRTY
        else:
            status = SYMBOL_CLEAN

        if repo.head.is_detached:
            branch = "detached"
        else:
            branch = repo.active_branch

        ui.info_count(
            i,
            len(repo_paths),
            status,
            f"[{branch}]",
            repo.working_dir,
        )


if __name__ == "__main__":
    main()
