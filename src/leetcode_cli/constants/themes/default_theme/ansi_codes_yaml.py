ANSI_CODES_YAML = """# This file defines ANSI escape codes used for styling text in the CLI.
# Each key is a name for a style/color, and the value is the actual escape code.

ANSI_CODES:
  RESET: "\\u001b[0m"                     # Resets all styles and colors to default - don't change this one;)

  # Standard Colors
  green: "\\u001b[38;2;80;250;123m"       # Green color using RGB values
  orange: "\\u001b[38;2;255;165;0m"       # Orange color using RGB values
  red: "\\u001b[38;2;255;85;85m"          # Red color using RGB values
  gray: "\\u001b[90m"                     # Gray text color
  white: "\\u001b[38;2;255;255;255m"      # White text color using RGB values
  black: "\\u001b[38;2;0;0;0m"            # Black text color using RGB values

  # Background Colors
  gray_bg: "\\u001b[100m"                 # Gray background color
  cyan_bg: "\\u001b[48;2;66;205;245m"     # Cyan background using RGB values
  orange_bg: "\\u001b[48;2;245;158;66m"   # Orange background using RGB values

  # Text Styles
  bold: "\\u001b[1m"                      # Bold text style
  italic: "\\u001b[3m"                    # Italic text style
  underline: "\\u001b[4m"                 # Underlined text style
"""
