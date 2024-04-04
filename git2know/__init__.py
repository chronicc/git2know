import os


# --------------------------------------------------------------------------------------
#
#   Version
#
# --------------------------------------------------------------------------------------
VERSION = "0.1.0"

# --------------------------------------------------------------------------------------
#
#   Paths
#
# --------------------------------------------------------------------------------------
CWD = os.getcwd()
HOME = os.environ["HOME"]
SOURCE = os.path.dirname(os.path.realpath(__file__))

# --------------------------------------------------------------------------------------
#
#   Configuration
#
# --------------------------------------------------------------------------------------
CONFIG_LOCATIONS = [
    f"{CWD}/.git2know.toml",
    f"{HOME}/.config/git2know/config.toml",
    f"{SOURCE}/config.toml",
]
for location in CONFIG_LOCATIONS:
    try:
        CONFIG = dict(config_from_toml(location, read_from_file=True))
        print(f"Loaded config from {location}")
        break
    except FileNotFoundError:
        CONFIG = dict({})
print(f"Config: {CONFIG}")

# Location of the index database
INDEX_DIR = CONFIG["default.index_dir"]
INDEX_FILE = f"{INDEX_DIR}/index.db"

# --------------------------------------------------------------------------------------
#
#   Symbols
#
# --------------------------------------------------------------------------------------
SYMBOL_CLEAN = "✓"
SYMBOL_DIRTY = "✗"
SYMBOL_UNPUSHED = "⤊"
SYMBOL_UNPULLED = "⤋"
