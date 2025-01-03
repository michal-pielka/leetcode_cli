ANSI_CODES_YAML = """# ansi_codes.yaml
#
# This file defines ANSI escape codes used for styling text in the CLI.
# Each key is a name for a style/color, and the value is the actual escape code.

ANSI_CODES:
  RESET: "\\u001b[0m"                     # Resets all styles and colors to default - don't change this one;)

  # Standard Colors
  green: "\\u001b[32m"                    # Green text color
  orange: "\\u001b[38;5;208m"             # Orange text color using 256-color mode
  red: "\\u001b[31m"                      # Red text color
  gray: "\\u001b[90m"                     # Gray text color
  white: "\\u001b[38;2;255;255;255m"      # White text color using RGB values
  black: "\\u001b[38;2;0;0;0m"            # Black text color using RGB values

  # Extended Green Shades
  GREEN1: "\\u001b[38;2;1;155;1m"         # Dark green shade
  GREEN2: "\\u001b[38;2;16;175;16m"       # Medium dark green shade
  GREEN3: "\\u001b[38;2;33;195;33m"       # Medium green shade
  GREEN4: "\\u001b[38;2;61;215;61m"       # Light green shade
  GREEN5: "\\u001b[38;2;82;235;82m"       # Very light green shade
  GREEN6: "\\u001b[38;2;100;255;100m"     # Neon green shade

  # Background Colors
  gray_bg: "\\u001b[100m"                 # Gray background color
  cyan_bg: "\\u001b[48;2;66;205;245m"     # Cyan background using RGB values
  orange_bg: "\\u001b[48;2;245;158;66m"   # Orange background using RGB values

  # Text Styles
  bold: "\\u001b[1m"                      # Bold text style
  italic: "\\u001b[3m"                    # Italic text style
  underline: "\\u001b[4m"                 # Underlined text style
"""
