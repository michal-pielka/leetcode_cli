# This file defines ANSI escape codes used for styling text in the Ayu theme.
# Each key is a name for a style/color, and the value is the actual escape code.

ANSI_CODES_YAML = """# ansi_codes.yaml
#
# This file defines ANSI escape codes used for styling text in the CLI.
# Each key is a name for a style/color, and the value is the actual escape code.

ANSI_CODES:
  RESET: "\\u001b[0m"                # Reset all styles

  # Colors
  ayu_mirage: "\\u001b[38;2;40;42;54m"  # Dark purple color for titles
  ayu_sapphire: "\\u001b[38;2;91;192;222m"  # Light blue for information
  ayu_flamingo: "\\u001b[38;2;255;121;198m" # Pink for highlights
  ayu_yellow: "\\u001b[38;2;255;209;102m"   # Yellow for warnings
  ayu_red: "\\u001b[38;2;255;85;85m"        # Red for errors
  ayu_gray: "\\u001b[38;2;136;136;136m"      # Gray for muted text
  ayu_white: "\\u001b[38;2;255;255;255m"     # White for general text
  ayu_black: "\\u001b[30m"                   # Black color for certain text elements
  ayu_pink: "\\u001b[38;2;255;121;198m"      # Pink color for highlights

  # Background Colors
  ayu_mirage_bg: "\\u001b[48;2;40;42;54m"    # Dark purple background for code blocks
  ayu_sapphire_bg: "\\u001b[48;2;91;192;222m" # Light blue background for tags
  ayu_flamingo_bg: "\\u001b[48;2;255;121;198m" # Pink background for certain elements
  ayu_orange_bg: "\\u001b[48;2;245;158;66m"   # Orange background for certain elements

  # Text Styles
  bold: "\\u001b[1m"                        # Bold text
  italic: "\\u001b[3m"                      # Italic text
  underline: "\\u001b[4m"                   # Underlined text
"""
