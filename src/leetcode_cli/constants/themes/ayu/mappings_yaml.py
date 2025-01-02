# This file unifies ANSI and symbol references under a single dictionary
# for each category (INTERPRETATION, SUBMISSION, PROBLEMSET, PROBLEM_DESCRIPTION, STATS_FORMATTER).
# Each key holds an 'ansi' (comma-separated style/color tokens) and an optional 'symbol'.
# These mappings are used to style various parts of the CLI application output,
# such as status messages, problem descriptions, and statistics.

MAPPINGS_YAML = """# mappings.yaml
#
# This file unifies ANSI and symbol references under a single dictionary
# for each category (INTERPRETATION, SUBMISSION, PROBLEMSET, PROBLEM_DESCRIPTION, STATS_FORMATTER).
# Each key holds an 'ansi' (comma-separated style/color tokens) and an optional 'symbol'.
# These mappings are used to style various parts of the CLI application output,
# such as status messages, problem descriptions, and statistics.

INTERPRETATION:
  # Status mappings for code interpretation results
  Accepted:
    ansi: "ayu_mirage,bold"            # Styles: Dark purple color and bold text for accepted submissions
    symbol: "checkmark"                # Symbol representing acceptance
  Wrong Answer:
    ansi: "ayu_red,bold"                # Styles: Red color and bold text for wrong answers
    symbol: "cross"                     # Symbol representing a wrong answer
  Memory Limit Exceeded:
    ansi: "ayu_red,bold"                # Styles: Red color and bold text for memory limit exceeded
    symbol: "cross"                     # Symbol representing memory limit exceeded
  Output Limit Exceeded:
    ansi: "ayu_red,bold"                # Styles: Red color and bold text for output limit exceeded
    symbol: "cross"                     # Symbol representing output limit exceeded
  Time Limit Exceeded:
    ansi: "ayu_red,bold"                # Styles: Red color and bold text for time limit exceeded
    symbol: "cross"                     # Symbol representing time limit exceeded
  Runtime Error:
    ansi: "ayu_red,bold"                # Styles: Red color and bold text for runtime errors
    symbol: "cross"                     # Symbol representing a runtime error
  Compile Error:
    ansi: "ayu_red,bold"                # Styles: Red color and bold text for compile errors
    symbol: "cross"                     # Symbol representing a compile error
  unknown:
    ansi: "ayu_yellow,bold"             # Styles: Yellow color and bold text for unknown statuses
    symbol: "cross"                     # Symbol representing an unknown status
  field:
    ansi: "ayu_white"                   # Styles: White color for field labels
    symbol: ""                           # No symbol for fields

SUBMISSION:
  # Status mappings for submission results
  Accepted:
    ansi: "ayu_mirage,bold"            # Styles: Dark purple color and bold text for accepted submissions
    symbol: "checkmark"                # Symbol representing acceptance
  Wrong Answer:
    ansi: "ayu_red,bold"                # Styles: Red color and bold text for wrong answers
    symbol: "cross"                     # Symbol representing a wrong answer
  Memory Limit Exceeded:
    ansi: "ayu_red,bold"                # Styles: Red color and bold text for memory limit exceeded
    symbol: "cross"                     # Symbol representing memory limit exceeded
  Output Limit Exceeded:
    ansi: "ayu_red,bold"                # Styles: Red color and bold text for output limit exceeded
    symbol: "cross"                     # Symbol representing output limit exceeded
  Time Limit Exceeded:
    ansi: "ayu_red,bold"                # Styles: Red color and bold text for time limit exceeded
    symbol: "cross"                     # Symbol representing time limit exceeded
  Runtime Error:
    ansi: "ayu_red,bold"                # Styles: Red color and bold text for runtime errors
    symbol: "cross"                     # Symbol representing a runtime error
  Compile Error:
    ansi: "ayu_red,bold"                # Styles: Red color and bold text for compile errors
    symbol: "cross"                     # Symbol representing a compile error
  unknown:
    ansi: "ayu_yellow,bold"             # Styles: Yellow color and bold text for unknown statuses
    symbol: "cross"                     # Symbol representing an unknown status
  field:
    ansi: "ayu_white"                   # Styles: White color for field labels
    symbol: ""                           # No symbol for fields

PROBLEMSET:
  # Mappings for styling problem list entries
  title:
    ansi: "ayu_mirage"                     # Styles: Dark purple color for titles
    symbol: ""                             # No symbol for title
  ac_rate:
    ansi: "ayu_white"                      # Styles: White color for acceptance rate percentages
    symbol: ""                             # No symbol for acceptance rate
  question_id:
    ansi: "ayu_white"                      # Styles: White color for question IDs
    symbol: ""                             # No symbol for question IDs
  Easy:
    ansi: "ayu_pink"                        # Styles: Pink color for easy difficulty labels
    symbol: ""                             # No symbol for easy difficulty labels
  Medium:
    ansi: "ayu_yellow"                      # Styles: Yellow color for medium difficulty labels
    symbol: ""                             # No symbol for medium difficulty labels
  Hard:
    ansi: "ayu_red"                         # Styles: Red color for hard difficulty labels
    symbol: ""                             # No symbol for hard difficulty labels
  ac:
    ansi: "ayu_mirage,bold"                # Styles: Dark purple color and bold text for accepted submissions
    symbol: "checkmark"                     # Symbol representing acceptance
  notac:
    ansi: "ayu_yellow"                      # Styles: Yellow color for attempted but not accepted submissions
    symbol: "snowflake"                     # Symbol representing an attempted submission
  not_started:
    ansi: "ayu_gray"                        # Styles: Gray color for not started status
    symbol: "space"                          # Symbol representing not started status
  field:
    ansi: "ayu_white,bold"                   # Styles: White color and bold text for field labels
    symbol: ""                               # No symbol for fields

PROBLEM_DESCRIPTION:
  # Mappings for styling problem descriptions
  strong:
    ansi: "bold"                             # Styles: Bold text for <strong> tags
    symbol: ""                               # No symbol for <strong> tags
  p:
    ansi: ""                                 # No ANSI styles for <p> tags
    symbol: ""                               # No symbol for <p> tags
  br:
    ansi: ""                                 # No ANSI styles for <br> tags
    symbol: ""                               # No symbol for <br> tags
  ul:
    ansi: ""                                 # No ANSI styles for <ul> tags
    symbol: ""                               # No symbol for <ul> tags
  li:
    ansi: ""                                 # No ANSI styles for <li> tags
    symbol: "dot"                            # Symbol representing list items
  sup:
    ansi: ""                                 # No ANSI styles for <sup> tags
    symbol: "caret"                          # Symbol representing superscripts
  b:
    ansi: "bold"                             # Styles: Bold text for <b> tags
    symbol: ""                               # No symbol for <b> tags
  em:
    ansi: "italic"                           # Styles: Italic text for <em> tags
    symbol: ""                               # No symbol for <em> tags
  i:
    ansi: "italic"                           # Styles: Italic text for <i> tags
    symbol: ""                               # No symbol for <i> tags
  u:
    ansi: "underline"                        # Styles: Underline text for <u> tags
    symbol: ""                               # No symbol for <u> tags
  span:
    ansi: ""                                 # No ANSI styles for <span> tags
    symbol: ""                               # No symbol for <span> tags
  ol:
    ansi: ""                                 # No ANSI styles for <ol> tags
    symbol: ""                               # No symbol for <ol> tags
  table:
    ansi: ""                                 # No ANSI styles for <table> tags
    symbol: ""                               # No symbol for <table> tags
  img:
    ansi: ""                                 # No ANSI styles for <img> tags
    symbol: ""                               # No symbol for <img> tags
  a:
    ansi: ""                                 # No ANSI styles for <a> tags
    symbol: ""                               # No symbol for <a> tags
  sub:
    ansi: ""                                 # No ANSI styles for <sub> tags
    symbol: ""                               # No symbol for <sub> tags
  blockquote:
    ansi: ""                                 # No ANSI styles for <blockquote> tags
    symbol: ""                               # No symbol for <blockquote> tags
  ptable:
    ansi: ""                                 # No ANSI styles for <ptable> tags
    symbol: ""                               # No symbol for <ptable> tags
  font:
    ansi: ""                                 # No ANSI styles for <font> tags
    symbol: ""                               # No symbol for <font> tags
  var:
    ansi: ""                                 # No ANSI styles for <var> tags
    symbol: ""                               # No symbol for <var> tags
  meta:
    ansi: ""                                 # No ANSI styles for <meta> tags
    symbol: ""                               # No symbol for <meta> tags
  div:
    ansi: ""                                 # No ANSI styles for <div> tags
    symbol: ""                               # No symbol for <div> tags
  style:
    ansi: ""                                 # No ANSI styles for <style> tags
    symbol: ""                               # No symbol for <style> tags
  code:
    ansi: "ayu_mirage_bg"                    # Styles: Dark purple background for <code> tags
    symbol: ""                               # No symbol for <code> tags
  pre:
    ansi: "ayu_red"                           # Styles: Red text for <pre> tags
    symbol: ""                               # No symbol for <pre> tags
  tag_label:
    ansi: "ayu_white,bold"                    # Styles: White color and bold text for "Tags:" label
    symbol: ""                               # No symbol for "Tags:" label
  tag:
    ansi: "ayu_sapphire_bg,ayu_white,bold"    # Styles: Cyan background, white color, and bold text for individual tags
    symbol: "space"                           # Symbol representing space between tags
  language_label:
    ansi: "ayu_white,bold"                    # Styles: White color and bold text for "Languages:" label
    symbol: ""                               # No symbol for "Languages:" label
  language:
    ansi: "ayu_orange_bg,ayu_black,bold"       # Styles: Orange background, black color, and bold text for programming languages
    symbol: "space"                           # Symbol representing space between languages
  title:
    ansi: "bold"                               # Styles: Bold text for problem titles
    symbol: ""                                 # No symbol for problem titles
  Easy:
    ansi: "ayu_pink"                           # Styles: Pink color for easy difficulty labels
    symbol: ""                                 # No symbol for easy difficulty labels
  Medium:
    ansi: "ayu_yellow"                         # Styles: Yellow color for medium difficulty labels
    symbol: ""                                 # No symbol for medium difficulty labels
  Hard:
    ansi: "ayu_red"                             # Styles: Red color for hard difficulty labels
    symbol: ""                                 # No symbol for hard difficulty labels
  example_title:
    ansi: "bold"                               # Styles: Bold text for example titles
    symbol: ""                                 # No symbol for example titles
  example_input_string:
    ansi: "bold"                               # Styles: Bold text for "Input:" labels
    symbol: ""                                 # No symbol for "Input:" labels
  example_output_string:
    ansi: "bold"                               # Styles: Bold text for "Output:" labels
    symbol: ""                                 # No symbol for "Output:" labels
  example_explanation_string:
    ansi: "bold"                               # Styles: Bold text for "Explanation:" labels
    symbol: ""                                 # No symbol for "Explanation:" labels
  example_input_data:
    ansi: "ayu_gray"                           # Styles: Gray text for example input data
    symbol: ""                                 # No symbol for example input data
  example_output_data:
    ansi: "ayu_gray"                           # Styles: Gray text for example output data
    symbol: ""                                 # No symbol for example output data
  example_explanation_data:
    ansi: "ayu_gray"                           # Styles: Gray text for example explanation data
    symbol: ""                                 # No symbol for example explanation data
  constraints_string:
    ansi: "bold"                               # Styles: Bold text for "Constraints:" labels
    symbol: ""                                 # No symbol for "Constraints:" labels
  field:
    ansi: "ayu_white,bold"                     # Styles: White color and bold text for field labels
    symbol: ""                                 # No symbol for fields

STATS_FORMATTER:
  # Mappings for styling user statistics and activity calendar
  EASY:
    ansi: "ayu_pink"                           # Styles: Pink color for easy difficulty stats
    symbol: ""                                 # No symbol for easy difficulty stats
  MEDIUM:
    ansi: "ayu_yellow"                         # Styles: Yellow color for medium difficulty stats
    symbol: ""                                 # No symbol for medium difficulty stats
  HARD:
    ansi: "ayu_red"                             # Styles: Red color for hard difficulty stats
    symbol: ""                                 # No symbol for hard difficulty stats
  CALENDAR_TIER0:
    ansi: "ayu_gray"                            # Styles: Gray color for calendar tier 0 (no activity)
    symbol: ""                                  # No symbol for calendar tier 0
  CALENDAR_TIER1:
    ansi: "ayu_orange,bold"                     # Styles: Orange color and bold text for calendar tier 1 (some activity)
    symbol: ""                                  # No symbol for calendar tier 1
  filled_square:
    ansi: ""                                     # No ANSI styles for filled squares in stats
    symbol: "filled_square"                     # Symbol representing filled squares
  empty_square:
    ansi: ""                                     # No ANSI styles for empty squares in stats
    symbol: "empty_square"                      # Symbol representing empty squares
  field:
    ansi: "ayu_white,bold"                      # Styles: White color and bold text for field labels
    symbol: ""                                  # No symbol for fields
"""
