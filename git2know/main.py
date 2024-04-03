#!/usr/bin/env python3

from git import GitCmdObjectDB, Repo
from git2know import SYMBOL_CLEAN, SYMBOL_DIRTY
from git2know.index import Index
from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.message import Message
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable


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

    def __str__(self) -> str:
        return self.repo.working_dir


class RepositoryDataTable(DataTable):
    """A widget displaying a list of repositories."""

    table_header = ("Status", "Path", "Branch")
    repositories = reactive([])

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.column_keys = self.add_columns(*self.table_header)

    def watch_repositories(self) -> None:
        print(self.repositories)

        old_rows = []
        for row_key in self.rows:
            old_rows.append(self.get_cell(row_key, self.column_keys[1]))
        print(old_rows)

        remove_rows = [x for x in old_rows if x not in self.repositories]
        print(remove_rows)
        for row in remove_rows:
            self.remove_row(row)

        add_rows = [x for x in self.repositories if x not in old_rows]
        print(add_rows)
        for i, row in enumerate(add_rows):
            label = Text(str(i + 1))
            repo = Repository(row)
            self.add_row(*repo.__repr__(), key=repo.__str__(), label=label)
        self.focus()


class RepositoryScreen(Screen):
    """The repository screen displaying the repository data table."""

    BINDINGS = [
        ("ctrl+r", "update_repositories", "Update repositories"),
        ("ctrl+u", "update_index", "Update file index"),
    ]

    class IndexUpdateTriggered(Message):

        def __init__(self) -> None:
            super().__init__()

    class RepositoryUpdateTriggered(Message):

        def __init__(self) -> None:
            super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(RepositoryDataTable())

    def on_mount(self) -> None:
        self.action_update_index()
        self.action_update_repositories()

    def action_update_index(self) -> None:
        print("Running action_update_index")
        self.post_message(self.IndexUpdateTriggered())

    def action_update_repositories(self) -> None:
        print("Running action_update_repositories")
        self.post_message(self.RepositoryUpdateTriggered())


class Git2KnowApp(App):
    """The main application."""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    SCREENS = {
        "main": RepositoryScreen(),
    }
    TITLE = "git2know"

    def toggle_dark(self) -> None:
        self.dark = not self.dark

    def on_mount(self) -> None:
        self.index = Index()
        self.push_screen("main")

    def on_repository_screen_index_update_triggered(
        self, message: RepositoryScreen.IndexUpdateTriggered
    ) -> None:
        print("Updating file index")
        self.index.update()
        self.query_one(RepositoryScreen).query_one(RepositoryDataTable).focus()
        print("File index updated")

    def on_repository_screen_repository_update_triggered(
        self, message: RepositoryScreen.RepositoryUpdateTriggered
    ) -> None:
        print("Updating repositories")
        self.query_one(RepositoryScreen).query_one(
            RepositoryDataTable
        ).repositories = self.index.read()
        print("Repositories updated")


def main():
    app = Git2KnowApp()
    app.run()


if __name__ == "__main__":
    main()
