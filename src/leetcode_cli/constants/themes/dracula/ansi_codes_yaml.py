# This file defines ANSI escape codes used for styling text in the Dracula theme.
# Each key is a name for a style/color, and the value is the actual escape code.

ANSI_CODES_YAML = """# ansi_codes.yaml
#
# This file defines ANSI escape codes used for styling text in the CLI.
# Each key is a name for a style/color, and the value is the actual escape code.

ANSI_CODES:
  RESET: "\\u001b[0m"                 # Reset all styles

  # Colors
  dracula_purple: "\\u001b[35m"       # Purple color for success messages
  dracula_cyan: "\\u001b[36m"         # Cyan color for informational messages
  dracula_orange: "\\u001b[38;5;208m" # Orange color for warnings
  dracula_red: "\\u001b[31m"          # Red color for error messages
  dracula_gray: "\\u001b[90m"         # Gray color for muted text
  dracula_white: "\\u001b[37m"        # White color for general text
  dracula_black: "\\u001b[30m"        # Black color for certain text elements
  dracula_yellow: "\\u001b[38;2;241;250;140m"  # Yellow color for highlights

  # Background Colors
  dracula_purple_bg: "\\u001b[45m"     # Purple background for code blocks
  dracula_cyan_bg: "\\u001b[46m"       # Cyan background for tags
  dracula_orange_bg: "\\u001b[48;5;208m" # Orange background for certain elements
  dracula_gray_bg: "\\u001b[47m"       # Gray background for highlighted sections

  # Text Styles
  bold: "\\u001b[1m"                   # Bold text
  italic: "\\u001b[3m"                 # Italic text
  underline: "\\u001b[4m"              # Underlined text
"""
