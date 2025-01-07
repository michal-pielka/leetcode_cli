MAPPINGS_YAML = """# This file unifies ANSI and symbol references under a single dictionary
# Each category (INTERPRETATION, SUBMISSION, PROBLEMSET, PROBLEM_DESCRIPTION, STATS_FORMATTER)
# contains keys that map to 'ansi' styles and symbols used in the CLI output.

INTERPRETATION: # Category for styling interpretation results
  # Status mappings for code interpretation results
  Accepted: # Status when a submission is accepted
    ansi: "green,bold"               # Green color and bold text indicate accepted submissions
    symbol_left: "checkmark,space"   # Symbols before the status: checkmark followed by a space
    symbol_right: ""                 # No symbol after the status
  Wrong Answer: # Status when the answer is wrong
    ansi: "red,bold"                 # Red color and bold text indicate wrong answers
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  Memory Limit Exceeded: # Status when memory limit is exceeded
    ansi: "red,bold"                 # Consistent red color and bold text
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  Output Limit Exceeded: # Status when output limit is exceeded
    ansi: "red,bold"                 # Consistent red color and bold text
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  Time Limit Exceeded: # Status when time limit is exceeded
    ansi: "red,bold"                 # Consistent red color and bold text
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  Runtime Error: # Status when a runtime error occurs
    ansi: "red,bold"                 # Consistent red color and bold text
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  Compile Error: # Status when a compile error occurs
    ansi: "red,bold"                 # Consistent red color and bold text
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  unknown: # Status for unknown results
    ansi: "orange,bold"              # Orange color and bold text indicate an unknown status
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  field_label: # Styling for field labels in interpretation
    ansi: "white"                    # White color for field labels
    symbol_left: ""                  # No symbol before the label
    symbol_right: "colon"            # Colon symbol after the label
  field_value: # Styling for field values in interpretation
    ansi: "white"                    # White color for field values
    symbol_left: ""                  # No symbol before the value
    symbol_right: ""                 # No symbol after the value

SUBMISSION: # Category for styling submission results, similar to INTERPRETATION
  # Status mappings for submission results
  Accepted: # Status when a submission is accepted
    ansi: "green,bold"               # Green color and bold text indicate accepted submissions
    symbol_left: "checkmark,space"   # Symbols before the status: checkmark followed by a space
    symbol_right: ""                 # No symbol after the status
  Wrong Answer: # Status when the answer is wrong
    ansi: "red,bold"                 # Red color and bold text indicate wrong answers
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  Memory Limit Exceeded: # Status when memory limit is exceeded
    ansi: "red,bold"                 # Consistent red color and bold text
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  Output Limit Exceeded: # Status when output limit is exceeded
    ansi: "red,bold"                 # Consistent red color and bold text
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  Time Limit Exceeded: # Status when time limit is exceeded
    ansi: "red,bold"                 # Consistent red color and bold text
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  Runtime Error: # Status when a runtime error occurs
    ansi: "red,bold"                 # Consistent red color and bold text
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  Compile Error: # Status when a compile error occurs
    ansi: "red,bold"                 # Consistent red color and bold text
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  unknown: # Status for unknown results
    ansi: "orange,bold"              # Orange color and bold text indicate an unknown status
    symbol_left: "cross,space"       # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  field_label: # Styling for field labels in submissions
    ansi: "white"                    # White color for field labels
    symbol_left: ""                  # No symbol before the label
    symbol_right: "colon"            # Colon symbol after the label
  field_value: # Styling for field values in submissions
    ansi: "white"                    # White color for field values
    symbol_left: ""                  # No symbol before the value
    symbol_right: ""                 # No symbol after the value

PROBLEMSET: # Category for styling problem set listings
  # Mappings for styling problem list entries
  title: # Styling for the title of the problem set
    ansi: "white"                      # White color for the title text
    symbol_left: ""                    # No symbol before the title
    symbol_right: ""                   # No symbol after the title
  acceptance_rate: # Styling for the acceptance rate display
    ansi: "white"                      # White color for acceptance rate
    symbol_left: "parenthesis_left"    # Left parenthesis symbol before the rate
    symbol_right: "percentage,parenthesis_right"  # Percentage symbol and right parenthesis after the rate
  question_id: # Styling for the question ID
    ansi: "white,bold"                 # White color and bold text for question ID
    symbol_left: "bracket_left"        # Left bracket before the ID
    symbol_right: "bracket_right"      # Right bracket after the ID
  Easy: # Styling for Easy difficulty label
    ansi: "green,bold"                 # Green color and bold text indicate Easy difficulty
    symbol_left: ""                    # No symbol before difficulty
    symbol_right: ""                   # No symbol after difficulty
  Medium: # Styling for Medium difficulty label
    ansi: "orange,bold"                # Orange color and bold text indicate Medium difficulty
    symbol_left: ""                    # No symbol before difficulty
    symbol_right: ""                   # No symbol after difficulty
  Hard: # Styling for Hard difficulty label
    ansi: "red,bold"                   # Red color and bold text indicate Hard difficulty
    symbol_left: ""                    # No symbol before difficulty
    symbol_right: ""                   # No symbol after difficulty
  ac: # Styling for accepted submissions count
    ansi: "green"                      # Green color for accepted submissions
    symbol_left: "checkmark"           # Checkmark symbol before the status
    symbol_right: ""                   # No symbol after the status
  notac: # Styling for not accepted submissions count
    ansi: "orange"                     # Orange color for not accepted submissions
    symbol_left: "snowflake"           # Snowflake symbol before the status
    symbol_right: ""                   # No symbol after the status
  not_started: # Styling for not started status
    ansi: ""                           # Default color implies white for not started status
    symbol_left: "space"               # Space before the status
    symbol_right: ""                   # No symbol after the status

PROBLEM_DESCRIPTION: # Category for styling problem descriptions
  # Mappings for styling problem descriptions
  strong: # Styling for strong text
    ansi: "bold"                        # Bold text
    symbol_left: ""                     # No symbol before strong text
    symbol_right: ""                    # No symbol after strong text
  p: # Styling for paragraphs
    ansi: ""                            # Default styling for paragraph
    symbol_left: ""                     # No symbol before the paragraph
    symbol_right: ""                  # Newline after paragraph
  br: # Styling for line breaks
    ansi: ""                            # No styling for line breaks
    symbol_left: ""                     # No symbol before the line break
    symbol_right: ""                  # Newline after line break
  ul: # Styling for unordered lists
    ansi: ""                            # Default styling for unordered lists
    symbol_left: ""                     # No symbol before the unordered list
    symbol_right: ""                    # No symbol after the unordered list
  li: # Styling for list items
    ansi: ""                            # Default styling for list items
    symbol_left: "dot"                  # Dot symbol before list item
    symbol_right: ""                    # No symbol after list item
  sup: # Styling for superscript text
    ansi: ""                            # No additional styling for superscript
    symbol_left: "caret"                # Caret symbol before superscript
    symbol_right: ""                    # No symbol after superscript
  b: # Styling for bold text
    ansi: "bold"                        # Bold text
    symbol_left: ""                     # No symbol before bold text
    symbol_right: ""                    # No symbol after bold text
  em: # Styling for emphasized text
    ansi: "italic"                      # Italic text
    symbol_left: ""                     # No symbol before emphasized text
    symbol_right: ""                    # No symbol after emphasized text
  i: # Styling for italic text
    ansi: "italic"                      # Italic text
    symbol_left: ""                     # No symbol before italic text
    symbol_right: ""                    # No symbol after italic text
  u: # Styling for underlined text
    ansi: "underline"                   # Underlined text
    symbol_left: ""                     # No symbol before underlined text
    symbol_right: ""                    # No symbol after underlined text
  span: # Styling for span elements
    ansi: ""                            # Default styling for span
    symbol_left: ""                     # No symbol before span
    symbol_right: ""                    # No symbol after span
  ol: # Styling for ordered lists
    ansi: ""                            # Default styling for ordered lists
    symbol_left: ""                     # No symbol before ordered list
    symbol_right: ""                    # No symbol after ordered list
  table: # Styling for tables
    ansi: ""                            # Default styling for tables
    symbol_left: ""                     # No symbol before table
    symbol_right: ""                    # No symbol after table
  img: # Styling for images
    ansi: ""                            # No styling for images
    symbol_left: ""                     # No symbol before image
    symbol_right: ""                    # No symbol after image
  a: # Styling for links
    ansi: ""                            # Default styling for links
    symbol_left: ""                     # No symbol before link
    symbol_right: ""                    # No symbol after link
  sub: # Styling for subscript text
    ansi: ""                            # No additional styling for subscript
    symbol_left: ""                     # No symbol before subscript
    symbol_right: ""                    # No symbol after subscript
  blockquote: # Styling for blockquotes
    ansi: ""                            # Default styling for blockquotes
    symbol_left: ""                     # No symbol before blockquote
    symbol_right: ""                    # No symbol after blockquote
  ptable: # Styling for property tables
    ansi: ""                            # Default styling for property tables
    symbol_left: ""                     # No symbol before property table
    symbol_right: ""                    # No symbol after property table
  font: # Styling for font tags
    ansi: ""                            # Default styling for font tags
    symbol_left: ""                     # No symbol before font tag
    symbol_right: ""                    # No symbol after font tag
  var: # Styling for variables
    ansi: ""                            # Default styling for variables
    symbol_left: ""                     # No symbol before variable
    symbol_right: ""                    # No symbol after variable
  meta: # Styling for meta tags
    ansi: ""                            # Default styling for meta tags
    symbol_left: ""                     # No symbol before meta tag
    symbol_right: ""                    # No symbol after meta tag
  div: # Styling for divs
    ansi: ""                            # Default styling for divs
    symbol_left: ""                     # No symbol before div
    symbol_right: ""                    # No symbol after div
  style: # Styling for style tags
    ansi: ""                            # No styling for style tags
    symbol_left: ""                     # No symbol before style tag
    symbol_right: ""                    # No symbol after style tag
  code: # Styling for inline code
    ansi: "gray_bg"                     # Gray background for inline code
    symbol_left: "space"                # Space before inline code
    symbol_right: "space"               # Space after inline code
  pre: # Styling for preformatted text
    ansi: "red"                         # Red color for preformatted text
    symbol_left: ""                     # No symbol before preformatted text
    symbol_right: ""                    # No symbol after preformatted text

  tag_label: # Styling for tag labels
    ansi: "white,bold"                  # Bold white text for tag labels
    symbol_left: ""                     # No symbol before tag label
    symbol_right: ""                    # No symbol after tag label
  tag: # Styling for tags
    ansi: "cyan_bg,white,bold"          # Cyan background with white bold text for tags
    symbol_left: "space"                # Space before the tag
    symbol_right: "space"               # Space after the tag
  language_label: # Styling for language labels
    ansi: "white,bold"                  # Bold white text for language labels
    symbol_left: ""                     # No symbol before language label
    symbol_right: ""                    # No symbol after language label
  language: # Styling for language tags
    ansi: "orange_bg,black,bold"        # Orange background with black bold text for languages
    symbol_left: "space"                # Space before the language
    symbol_right: "space"               # Space after the language
  title: # Styling for titles within problem descriptions
    ansi: "white,bold"                  # Bold white text for titles
    symbol_left: ""                     # No symbol before the title
    symbol_right: ""                    # No symbol after the title
  Easy: # Styling for Easy difficulty within problem descriptions
    ansi: "green,bold"                  # Bold green text for Easy difficulty
    symbol_left: "bracket_left"         # Left bracket before difficulty
    symbol_right: "bracket_right"       # Right bracket after difficulty
  Medium: # Styling for Medium difficulty within problem descriptions
    ansi: "orange,bold"                 # Bold orange text for Medium difficulty
    symbol_left: "bracket_left"         # Left bracket before difficulty
    symbol_right: "bracket_right"       # Right bracket after difficulty
  Hard: # Styling for Hard difficulty within problem descriptions
    ansi: "red,bold"                    # Bold red text for Hard difficulty
    symbol_left: "bracket_left"         # Left bracket before difficulty
    symbol_right: "bracket_right"       # Right bracket after difficulty
  example_title: # Styling for example titles
    ansi: "bold"                        # Bold text for example titles
    symbol_left: ""                     # No symbol before example title
    symbol_right: ""                    # No symbol after example title
  example_input_string: # Styling for "Input" label in examples
    ansi: "bold"                        # Bold text for "Input" label
    symbol_left: "pipe,space"                     # No symbol before "Input" label
    symbol_right: "colon,space"                    # No symbol after "Input" label
  example_output_string: # Styling for "Output" label in examples
    ansi: "bold"                        # Bold text for "Output" label
    symbol_left: "pipe,space"                     # No symbol before "Output" label
    symbol_right: "colon,space"                    # No symbol after "Output" label
  example_explanation_string: # Styling for "Explanation" label in examples
    ansi: "bold"                        # Bold text for "Explanation" label
    symbol_left: "pipe,space"                     # No symbol before "Explanation" label
    symbol_right: "colon,space"                    # No symbol after "Explanation" label
  example_input_data: # Styling for example input data
    ansi: "gray"                        # Gray text for input data
    symbol_left: ""                     # No symbol before input data
    symbol_right: ""                    # No symbol after input data
  example_output_data: # Styling for example output data
    ansi: "gray"                        # Gray text for output data
    symbol_left: ""                     # No symbol before output data
    symbol_right: ""                    # No symbol after output data
  example_explanation_data: # Styling for example explanation data
    ansi: "gray"                        # Gray text for explanation data
    symbol_left: ""                     # No symbol before explanation data
    symbol_right: ""                    # No symbol after explanation data
  constraints_string: # Styling for "Constraints" label
    ansi: "bold"                        # Bold text for "Constraints" label
    symbol_left: ""                     # No symbol before "Constraints" label
    symbol_right: ""                    # No symbol after "Constraints" label

STATS: # Category for styling user statistics and activity calendar
  # Mappings for styling user statistics and activity calendar
  EASY: # Styling for Easy solved problems count
    ansi: "green"                       # Green color for Easy solved problems
    symbol_left: ""                     # No symbol before Easy count
    symbol_right: ""                    # No symbol after Easy count
  MEDIUM: # Styling for Medium solved problems count
    ansi: "orange"                      # Orange color for Medium solved problems
    symbol_left: ""                     # No symbol before Medium count
    symbol_right: ""                    # No symbol after Medium count
  HARD: # Styling for Hard solved problems count
    ansi: "red"                         # Red color for Hard solved problems
    symbol_left: ""                     # No symbol before Hard count
    symbol_right: ""                    # No symbol after Hard count
  CALENDAR_TIER0: # Styling for lowest tier in calendar
    ansi: "gray"                        # Gray color for lowest tier in calendar
    symbol_left: ""                     # No symbol before tier
    symbol_right: ""                    # No symbol after tier
  CALENDAR_TIER1: # Styling for higher tier in calendar
    ansi: "orange,bold"                 # Bold orange color for higher tier in calendar
    symbol_left: ""                     # No symbol before tier
    symbol_right: ""                    # No symbol after tier
  filled_square: # Styling for filled squares in calendar
    ansi: ""                            # Default color for filled squares
    symbol_left: "filled_square"        # Filled square symbol
    symbol_right: ""                    # No symbol after filled square
  empty_square: # Styling for empty squares in calendar
    ansi: ""                            # Default color for empty squares
    symbol_left: "empty_square"         # Empty square symbol
    symbol_right: ""                    # No symbol after empty square
  field: # Styling for statistical fields
    ansi: "white,bold"                  # Bold white text for statistical fields
    symbol_left: ""                     # No symbol before field
    symbol_right: ""                    # No symbol after field
"""
