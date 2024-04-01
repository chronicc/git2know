#!/usr/bin/env python3

from git2know.classes.repository import Repository
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
        repo = Repository(path)
        branch = f"[{repo.branch}]"
        if repo.status == "uncommited":
            ui.info_count(i, len(repo_paths), SYMBOL_UNCOMMITED, branch, path)
        elif repo.status == "unpushed":
            ui.info_count(i, len(repo_paths), SYMBOL_UNPUSHED, branch, path)
        else:
            ui.info_count(i, len(repo_paths), ui.check, branch, path)
    ui.info("")
    ui.info_section("Key")
    ui.info(ui.check, " up-to-date")
    ui.info(SYMBOL_UNPUSHED, " unpushed changes")
    ui.info(SYMBOL_UNCOMMITED, " uncommited changes")
    ui.info(SYMBOL_UNPULLED, " unpulled changes (not yet implemented)")


if __name__ == "__main__":
    main()
