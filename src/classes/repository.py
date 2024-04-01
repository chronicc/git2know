import os
import re
from subprocess import check_output


class Repository:

    branch = None
    path = None
    status = None

    def __init__(self, path):
        self.path = os.path.split(path)[0]
        self.update()

    def update(self):
        self.branch = (
            check_output(
                ["git", "branch", "--show-current", "--no-color"], cwd=self.path
            )
            .decode()
            .strip()
        )
        status = (
            check_output(["git", "status", "--porcelain"], cwd=self.path)
            .decode()
            .strip()
            .split("\n")
        )
        if status == [""]:
            self.status = "ok"
            return
        for state in status:
            if re.match(r"(^[A ]+M|^\?\?)", state):
                self.status = "uncommited"
                return
        self.status = "unpushed"
