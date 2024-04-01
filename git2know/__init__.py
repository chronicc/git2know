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
HOME = os.environ["HOME"]
INDEXDB = f"{HOME}/.cache/mlocate.db"

# --------------------------------------------------------------------------------------
#
#   Symbols
#
# --------------------------------------------------------------------------------------
SYMBOL_CLEAN = "✓"
SYMBOL_DIRTY = "✗"
SYMBOL_UNPUSHED = "⤊"
SYMBOL_UNPULLED = "⤋"