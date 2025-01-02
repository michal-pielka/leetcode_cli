# This file defines ANSI escape codes used for styling text in the Monokai theme.
# Each key is a name for a style/color, and the value is the actual escape code.

ANSI_CODES_YAML = """# ansi_codes.yaml
#
# This file defines ANSI escape codes used for styling text in the CLI.
# Each key is a name for a style/color, and the value is the actual escape code.

ANSI_CODES:
  RESET: "\\u001b[0m"                 # Reset all styles

  # Colors
  monokai_green: "\\u001b[32m"        # Green color for success messages
  monokai_yellow: "\\u001b[33m"       # Yellow color for warnings
  monokai_pink: "\\u001b[35m"         # Pink color for highlights
  monokai_blue: "\\u001b[34m"         # Blue color for informational messages
  monokai_red: "\\u001b[31m"          # Red color for error messages
  monokai_gray: "\\u001b[90m"         # Gray color for muted text
  monokai_white: "\\u001b[37m"        # White color for general text
  monokai_black: "\\u001b[30m"        # Black color for certain text elements

  # Background Colors
  monokai_gray_bg: "\\u001b[100m"      # Gray background for code blocks
  monokai_blue_bg: "\\u001b[44m"       # Blue background for tags
  monokai_orange_bg: "\\u001b[48;2;245;158;66m"  # Orange background for certain elements

  # Text Styles
  bold: "\\u001b[1m"                   # Bold text
  italic: "\\u001b[3m"                 # Italic text
  underline: "\\u001b[4m"              # Underlined text
"""
