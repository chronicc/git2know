import cli_ui as ui
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
SYMBOL_CLEAN = ui.UnicodeSequence(ui.darkgreen, "✓", "c")
SYMBOL_DIRTY = ui.UnicodeSequence(ui.darkred, "✗", "d")
SYMBOL_UNPUSHED = ui.UnicodeSequence(ui.darkyellow, "⤊", "+")
SYMBOL_UNPULLED = ui.UnicodeSequence(ui.darkblue, "⤋", "-")
