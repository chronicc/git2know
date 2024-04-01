# git2know

A cli dashboard to supply information about all git repositories in the users home
directory.

## Getting started

The current version finds all local git repositories and prints out a list of the
respective status of each repository, differentiating between uncommited, unpushed and
up-to-date.

- Install [mise](https://mise.jdx.dev/getting-started.html)
- Run `mise run install`
- Run `git2know`

## Documentation

- [Conventional Commits](./docs/conventional-commits.md)

## How it works

git2know uses

* **mlocate** to create a list of all git repositories on the local machine

### mlocate

The application creates an mlocate database in your default cache directory
(`$HOME/.cache/mlocate.db`). This database is updated on every run. The way mlocate
works only changes will be comitted to the database on each run so the first run of the
application might take some seconds or minutes depending on the size of your home
directory. The mlocate database is not limited to this application and only stores an
index of all files contained in your home directory. You are free to use this database
with other applications relying on mlocate.

## Goals

* Get an overview of all git repositories on the system.
* Provide a query language for filtering repositories and finding information.

## License

MIT
