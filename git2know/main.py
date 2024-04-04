#!/usr/bin/env python3

from config import config_from_toml, Configuration
from git2know import CONFIG_LOCATIONS
from git2know.index import Index
from git2know.repository import RepositoryDataTable, RepositoryScreen
from textual.app import App
from textual.binding import Binding


class Git2KnowApp(App):
    """The main application."""

    BINDINGS = [
        Binding(
            action="toggle_dark",
            description="Toggle dark mode",
            key="d",
        ),
        # TODO: Add help screen
        # Binding(
        #     action="help",
        #     description="Show help screen",
        #     key_display="?",
        #     key="question_mark",
        # ),
    ]
    SCREENS = {
        "main": RepositoryScreen(),
    }
    TITLE = "git2know"

    config: Configuration
    index: Index

    def __init__(self) -> None:
        super().__init__()

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
