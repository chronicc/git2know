from git2know import config
from subprocess import check_call, check_output
import os
import shutil


class Index:

    def __init__(self) -> None:
        if not os.path.exists(config.cache_dir):
            os.makedirs(config.cache_dir)

    def read(self) -> list[str]:
        common_args = [
            "--database",
            f"{config.cache_dir}/index.db",
            "--regexp",
            "^.*/.git$",
        ]
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
