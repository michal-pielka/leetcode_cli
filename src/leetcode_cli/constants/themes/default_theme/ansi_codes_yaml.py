ANSI_CODES_YAML = """# ansi_codes.yaml
#
# This file defines ANSI escape codes used for styling text in the CLI.
# Each key is a name for a style/color, and the value is the actual escape code.

ANSI_CODES:
  RESET: "\\u001b[0m"

  green: "\\u001b[32m"
  orange: "\\u001b[38;5;208m"
  red: "\\u001b[31m"
  gray: "\\u001b[90m"
  white: "\\u001b[38;2;255;255;255m"
  black: "\\u001b[38;2;0;0;0m"

  GREEN1: "\\u001b[38;2;1;155;1m"
  GREEN2: "\\u001b[38;2;16;175;16m"
  GREEN3: "\\u001b[38;2;33;195;33m"
  GREEN4: "\\u001b[38;2;61;215;61m"
  GREEN5: "\\u001b[38;2;82;235;82m"
  GREEN6: "\\u001b[38;2;100;255;100m"

  gray_bg: "\\u001b[100m"
  cyan_bg: "\\u001b[48;2;66;205;245m"
  orange_bg: "\\u001b[48;2;245;158;66m"

  bold: "\\u001b[1m"
  italic: "\\u001b[3m"
  underline: "\\u001b[4m"
"""
