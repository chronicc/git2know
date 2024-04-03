from git2know import HOME, INDEX_DIR, INDEX_FILE
from subprocess import check_call, check_output
import os
import shutil


class Index:

    def __init__(self) -> None:
        if not os.path.exists(INDEX_DIR):
            os.makedirs(INDEX_DIR)

    def read(self) -> list[str]:
        common_args = ["--database", INDEX_FILE, "--regexp", "^.*/.git$"]
        if shutil.which("mlocate"):
            search_cmd = ["mlocate", "-q"]
        elif shutil.which("locate"):
            search_cmd = ["locate"]
        else:
            raise Exception(
                "No binary for reading the mlocate database found."
                "Please install mlocate or locate."
            )
        entries = check_output(search_cmd + common_args).decode().strip().split("\n")
        for i, path in enumerate(entries):
            entries[i] = path[:-4]
        return entries

    def update(self) -> None:
        check_call(
            [
                "updatedb",
                "--add-prunenames",
                f".cache .local .pulumi .pyenv",
                "--database-root",
                HOME,
                "--output",
                INDEX_FILE,
                "--require-visibility",
                "0",
            ]
        )
