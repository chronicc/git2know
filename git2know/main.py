#!/usr/bin/env python3

from git import GitCmdObjectDB, Repo
from git2know import HOME, INDEXDB, SYMBOL_CLEAN, SYMBOL_DIRTY
from rich.text import Text
from subprocess import check_call, check_output
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Header, Footer, DataTable
import shutil


class Repository:
    """A widget displaying information about a repository."""

    def __init__(self, path: str) -> None:
        self.repo = Repo(path, odbt=GitCmdObjectDB)
        super().__init__()

    def __repr__(self) -> str:
        if self.repo.is_dirty():
            status = SYMBOL_DIRTY
        else:
            status = SYMBOL_CLEAN
        if self.repo.head.is_detached:
            branch = "~detached~"
        else:
            branch = self.repo.active_branch
        return (status, self.repo.working_dir, branch)


class RepositoryList(DataTable):
    """A widget displaying a list of repositories."""

    table_header = ("Status", "Path", "Branch")
    repositories = reactive([])

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.add_columns(*self.table_header)

    def watch_repositories(self) -> None:
        self.clear()
        for i, repo in enumerate(self.repositories):
            label = Text(str(i + 1))
            self.add_row(*repo.__repr__(), label=label)
        self.focus()


class Git2KnowApp(App):
    """The main application."""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("ctrl+u", "update_repositories", "Update repositories"),
    ]

    TITLE = "git2know"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(RepositoryList())

    def toggle_dark(self) -> None:
        self.dark = not self.dark

    def on_mount(self) -> None:
        self.action_update_repositories()

    def action_update_repositories(self) -> None:
        print("Running action_update_repositories")
        check_call(
            [
                "updatedb",
                "--add-prunenames",
                f".cache .local .pulumi .pyenv",
                "--database-root",
                HOME,
                "--output",
                INDEXDB,
                "--require-visibility",
                "0",
            ]
        )
        common_args = ["-d", INDEXDB, "-r", "^.*/.git$"]
        if shutil.which("mlocate"):
            search_cmd = ["mlocate", "-q"]
        elif shutil.which("locate"):
            search_cmd = ["locate"]
        else:
            raise Exception(
                "No binary for reading the mlocate database found."
                "Please install mlocate or locate."
            )
        repo_paths = check_output(search_cmd + common_args).decode().strip().split("\n")
        repos = []
        for _, path in enumerate(repo_paths):
            repos.append(Repository(path))
        self.query_one(RepositoryList).repositories = repos
        print("Finished running action_update_repositories")


def main():
    app = Git2KnowApp()
    app.run()


if __name__ == "__main__":
    main()
