ANSI_CODES_YAML = """# ansi_codes.yaml
#
# This file defines ANSI escape codes used for styling text in the CLI.
# Each key is a name for a style/color, and the value is the actual escape code.

ANSI_CODES:
  RESET: "\\u001b[0m"

  GREEN: "\\u001b[32m"
  ORANGE: "\\u001b[38;5;208m"
  RED: "\\u001b[31m"
  GRAY: "\\u001b[90m"
  CYAN: "\\u001b[96m"
  WHITE: "\\u001b[38;2;255;255;255m"
  BLACK: "\\u001b[38;2;0;0;0m"

  GREEN1: "\\u001b[38;2;1;155;1m"
  GREEN2: "\\u001b[38;2;16;175;16m"
  GREEN3: "\\u001b[38;2;33;195;33m"
  GREEN4: "\\u001b[38;2;61;215;61m"
  GREEN5: "\\u001b[38;2;82;235;82m"
  GREEN6: "\\u001b[38;2;100;255;100m"

  GRAY_BG: "\\u001b[100m"
  GREEN_BG: "\\u001b[42m"
  BABY_BLUE_BG: "\\u001b[48;2;66;205;245m"
  RED_BG: "\\u001b[41m"
  ORANGE_BG: "\\u001b[48;2;245;158;66m"

  BOLD: "\\u001b[1m"
  ITALIC: "\\u001b[3m"
  UNDERLINE: "\\u001b[4m"

  EMPTY: ""
"""
