MAPPINGS_YAML = """# mappings.yaml
#
# This file maps the above ANSI_CODES and SYMBOLS to various CLI contexts:
# - Interpretation
# - Problemset
# - Submission
# - Problem formatting
# - Stats formatting

INTERPRETATION_ANSI_CODES:
  Accepted: "GREEN,BOLD"
  Wrong Answer: "RED,BOLD"
  Memory Limit Exceeded: "RED,BOLD"
  Output Limit Exceeded: "RED,BOLD"
  Time Limit Exceeded: "RED,BOLD"
  Runtime Error: "RED,BOLD"
  Compile Error: "RED,BOLD"
  unknown: "ORANGE,BOLD"

INTERPRETATION_SYMBOLS:
  Accepted: "CHECKMARK"
  Wrong Answer: "X"
  Memory Limit Exceeded: "X"
  Output Limit Exceeded: "X"
  Time Limit Exceeded: "X"
  Runtime Error: "X"
  Compile Error: "X"
  unknown: "X"

PROBLEMSET_FORMATTER_ANSI_CODES:
  Easy: "GREEN"
  Medium: "ORANGE"
  Hard: "RED"
  ac: "GREEN"
  notac: "ORANGE"
  not_started: "GRAY"

PROBLEMSET_FORMATTER_SYMBOLS:
  Easy: "EMPTY"
  Medium: "EMPTY"
  Hard: "EMPTY"
  ac: "CHECKMARK"
  notac: "ATTEMPTED"
  not_started: "SPACE"

SUBMISSION_ANSI_CODES:
  Accepted: "GREEN,BOLD"
  Wrong Answer: "RED,BOLD"
  Memory Limit Exceeded: "RED,BOLD"
  Output Limit Exceeded: "RED,BOLD"
  Time Limit Exceeded: "RED,BOLD"
  Runtime Error: "RED,BOLD"
  Compile Error: "RED,BOLD"
  unknown: "ORANGE,BOLD"

SUBMISSION_SYMBOLS:
  Accepted: "CHECKMARK"
  Wrong Answer: "X"
  Memory Limit Exceeded: "X"
  Output Limit Exceeded: "X"
  Time Limit Exceeded: "X"
  Runtime Error: "X"
  Compile Error: "X"
  unknown: "X"

PROBLEM_FORMATTER_ANSI_CODES:
  strong: "BOLD"
  p: "EMPTY"
  br: "EMPTY"
  ul: "EMPTY"
  li: "EMPTY"
  sup: "EMPTY"
  b: "BOLD"
  em: "ITALIC"
  i: "ITALIC"
  u: "UNDERLINE"

  span: "EMPTY"
  ol: "EMPTY"
  table: "EMPTY"
  img: "EMPTY"
  a: "EMPTY"
  sub: "EMPTY"
  blockquote: "EMPTY"
  ptable: "EMPTY"
  font: "EMPTY"
  var: "EMPTY"
  meta: "EMPTY"
  div: "EMPTY"
  style: "EMPTY"

  code: "GRAY_BG"
  pre: "RED"
  tag: "BABY_BLUE_BG,WHITE,BOLD"
  language: "ORANGE_BG,BLACK,BOLD"
  title: "BOLD"
  Easy: "GREEN"
  Medium: "ORANGE"
  Hard: "RED"
  example_title: "BOLD"
  example_input_string: "BOLD"
  example_output_string: "BOLD"
  example_explanation_string: "BOLD"
  example_input_data: "GRAY"
  example_output_data: "GRAY"
  example_explanation_data: "GRAY"
  constraints_string: "BOLD"

PROBLEM_FORMATTER_SYMBOLS:
  strong: "EMPTY"
  p: "EMPTY"
  br: "EMPTY"
  ul: "EMPTY"
  li: "DOT"
  sup: "CARET"
  b: "EMPTY"
  em: "EMPTY"
  i: "EMPTY"
  u: "EMPTY"

  span: "EMPTY"
  ol: "EMPTY"
  table: "EMPTY"
  img: "EMPTY"
  a: "EMPTY"
  sub: "EMPTY"
  blockquote: "EMPTY"
  ptable: "EMPTY"
  font: "EMPTY"
  var: "EMPTY"
  meta: "EMPTY"
  div: "EMPTY"
  style: "EMPTY"

  code: "EMPTY"
  pre: "EMPTY"
  tag: "EMPTY"
  language: "EMPTY"
  title: "EMPTY"
  Easy: "EMPTY"
  Medium: "EMPTY"
  Hard: "EMPTY"
  example_title: "EMPTY"
  example_input_string: "EMPTY"
  example_output_string: "EMPTY"
  example_explanation_string: "EMPTY"
  example_input_data: "EMPTY"
  example_output_data: "EMPTY"
  example_explanation_data: "EMPTY"
  constraints_string: "EMPTY"

STATS_FORMATTER_DIFFICULTY_COLORS:
  EASY: "GREEN"
  MEDIUM: "ORANGE"
  HARD: "RED"
  CALENDAR_TIER0: "GRAY"

STATS_FORMATTER_SYMBOLS:
  EASY: "EMPTY"
  MEDIUM: "EMPTY"
  HARD: "EMPTY"
  CALENDAR_TIER0: "EMPTY"
  FILLED_SQUARE: "FILLED_SQUARE"
  EMPTY_SQUARE: "EMPTY_SQUARE"
"""

