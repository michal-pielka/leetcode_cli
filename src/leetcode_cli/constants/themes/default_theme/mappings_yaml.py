MAPPINGS_YAML = """# This file unifies ANSI and symbol references under a single dictionary
# Each category (INTERPRETATION, SUBMISSION, PROBLEMSET, PROBLEM_DESCRIPTION, STATS_FORMATTER)
# contains keys that map to 'ansi' styles and symbols used in the CLI output.

INTERPRETATION:
  # Status mappings for code interpretation results
  Accepted:
    ansi: "green,bold"               # Green color and bold text indicate accepted submissions
    symbol_left: "checkmark,space"   # Symbols before the status: checkmark followed by a space
    symbol_right: ""                 # No symbol after the status
  Wrong Answer:
    ansi: "red,bold"                 # Red color and bold text indicate wrong answers
    symbol_left: "cross,space"        # Symbols before the status: cross followed by a space
    symbol_right: ""                 # No symbol after the status
  Memory Limit Exceeded:
    ansi: "red,bold"                 # Consistent styling for memory limit issues
    symbol_left: "cross,space"
    symbol_right: ""
  Output Limit Exceeded:
    ansi: "red,bold"                 # Consistent styling for output limit issues
    symbol_left: "cross,space"
    symbol_right: ""
  Time Limit Exceeded:
    ansi: "red,bold"                 # Consistent styling for time limit issues
    symbol_left: "cross,space"
    symbol_right: ""
  Runtime Error:
    ansi: "red,bold"                 # Consistent styling for runtime errors
    symbol_left: "cross,space"
    symbol_right: ""
  Compile Error:
    ansi: "red,bold"                 # Consistent styling for compile errors
    symbol_left: "cross,space"
    symbol_right: ""
  unknown:
    ansi: "orange,bold"              # Orange color indicates an unknown status
    symbol_left: "cross,space"
    symbol_right: ""
  field_label:
    ansi: "white"                    # White color for field labels
    symbol_left: ""                  # No symbol before the label
    symbol_right: "colon"            # Colon symbol after the label
  field_value:
    ansi: "green"                    # Green color for field values
    symbol_left: ""                  # No symbol before the value
    symbol_right: ""                 # No symbol after the value

SUBMISSION:
  # Status mappings for submission results, similar to INTERPRETATION
  Accepted:
    ansi: "green,bold"
    symbol_left: "checkmark,space"
    symbol_right: ""
  Wrong Answer:
    ansi: "red,bold"
    symbol_left: "cross,space"
    symbol_right: ""
  Memory Limit Exceeded:
    ansi: "red,bold"
    symbol_left: "cross,space"
    symbol_right: ""
  Output Limit Exceeded:
    ansi: "red,bold"
    symbol_left: "cross,space"
    symbol_right: ""
  Time Limit Exceeded:
    ansi: "red,bold"
    symbol_left: "cross,space"
    symbol_right: ""
  Runtime Error:
    ansi: "red,bold"
    symbol_left: "cross,space"
    symbol_right: ""
  Compile Error:
    ansi: "red,bold"
    symbol_left: "cross,space"
    symbol_right: ""
  unknown:
    ansi: "orange,bold"
    symbol_left: "cross,space"
    symbol_right: ""
  field_label:
    ansi: "white"                    # White color for field labels
    symbol_left: ""                  # No symbol before the label
    symbol_right: "colon"            # Colon symbol after the label
  field_value:
    ansi: "white"                    # White color for field values
    symbol_left: ""                  # No symbol before the value
    symbol_right: ""                 # No symbol after the value

PROBLEMSET:
  # Mappings for styling problem list entries
  title:
    ansi: "white"                      # White color for the title text
    symbol_left: ""                    # No symbol before the title
    symbol_right: ""                   # No symbol after the title
  acceptance_rate:
    ansi: "white"                      # White color for acceptance rate
    symbol_left: "parenthesis_left"    # Left parenthesis symbol before the rate
    symbol_right: "percentage,parenthesis_right"  # Percentage and right parenthesis after the rate
  question_id:
    ansi: "white"                      # White color for question ID
    symbol_left: "bracket_left"        # Left bracket before the ID
    symbol_right: "bracket_right"      # Right bracket after the ID
  Easy:
    ansi: "green"                      # Green color indicates Easy difficulty
    symbol_left: ""                    # No symbol before difficulty
    symbol_right: ""                   # No symbol after difficulty
  Medium:
    ansi: "orange"                     # Orange color indicates Medium difficulty
    symbol_left: ""                    
    symbol_right: ""
  Hard:
    ansi: "red"                        # Red color indicates Hard difficulty
    symbol_left: ""
    symbol_right: ""
  ac:
    ansi: "green"                      # Green color for accepted submissions
    symbol_left: "checkmark"           # Checkmark symbol before the status
    symbol_right: ""                   # No symbol after the status
  notac:
    ansi: "orange"                     # Orange color for not accepted submissions
    symbol_left: "snowflake"           # Snowflake symbol before the status
    symbol_right: ""                   
  not_started:
    ansi: ""                           # Default color implies white for not started status
    symbol_left: "space"               # Space before the status
    symbol_right: ""                   

PROBLEM_DESCRIPTION:
  # Mappings for styling problem descriptions
  strong:
    ansi: "bold"                       # Bold text
    symbol_left: ""                    
    symbol_right: ""
  p:
    ansi: ""                            # Default styling for paragraph
    symbol_left: ""
    symbol_right: "\n"                  # Newline after paragraph
  br:
    ansi: ""                            # No styling for line breaks
    symbol_left: ""
    symbol_right: "\n"                  # Newline after line break
  ul:
    ansi: ""                            # Default styling for unordered lists
    symbol_left: ""
    symbol_right: ""
  li:
    ansi: ""                            # Default styling for list items
    symbol_left: "dot"                  # Dot symbol before list item
    symbol_right: ""                    
  sup:
    ansi: ""                            # No additional styling for superscript
    symbol_left: "caret"                # Caret symbol before superscript
    symbol_right: ""                    
  b:
    ansi: "bold"                        # Bold text
    symbol_left: ""
    symbol_right: ""
  em:
    ansi: "italic"                      # Italic text
    symbol_left: ""
    symbol_right: ""
  i:
    ansi: "italic"                      # Italic text
    symbol_left: ""
    symbol_right: ""
  u:
    ansi: "underline"                   # Underlined text
    symbol_left: ""
    symbol_right: ""
  span:
    ansi: ""                            # Default styling for span
    symbol_left: ""
    symbol_right: ""
  ol:
    ansi: ""                            # Default styling for ordered lists
    symbol_left: ""
    symbol_right: ""
  table:
    ansi: ""                            # Default styling for tables
    symbol_left: ""
    symbol_right: ""
  img:
    ansi: ""                            # No styling for images
    symbol_left: ""
    symbol_right: ""
  a:
    ansi: ""                            # Default styling for links
    symbol_left: ""
    symbol_right: ""
  sub:
    ansi: ""                            # No additional styling for subscript
    symbol_left: ""
    symbol_right: ""
  blockquote:
    ansi: ""                            # Default styling for blockquotes
    symbol_left: ""
    symbol_right: ""
  ptable:
    ansi: ""                            # Default styling for property tables
    symbol_left: ""
    symbol_right: ""
  font:
    ansi: ""                            # Default styling for font tags
    symbol_left: ""
    symbol_right: ""
  var:
    ansi: ""                            # Default styling for variables
    symbol_left: ""
    symbol_right: ""
  meta:
    ansi: ""                            # Default styling for meta tags
    symbol_left: ""
    symbol_right: ""
  div:
    ansi: ""                            # Default styling for divs
    symbol_left: ""
    symbol_right: ""
  style:
    ansi: ""                            # No styling for style tags
    symbol_left: ""
    symbol_right: ""
  code:
    ansi: "gray_bg"                     # Gray background for inline code
    symbol_left: "space"                # Space before inline code
    symbol_right: "space"               # Space after inline code
  pre:
    ansi: "red"                         # Red color for preformatted text
    symbol_left: ""                     # No symbol before preformatted text
    symbol_right: ""                    # No symbol after preformatted text

  tag_label:
    ansi: "white,bold"                  # Bold white text for tag labels
    symbol_left: ""
    symbol_right: ""                    
  tag:
    ansi: "cyan_bg,white,bold"          # Cyan background with white bold text for tags
    symbol_left: "space"                # Space before the tag
    symbol_right: "space"               # Space after the tag
  language_label:
    ansi: "white,bold"                  # Bold white text for language labels
    symbol_left: ""
    symbol_right: ""                    
  language:
    ansi: "orange_bg,black,bold"        # Orange background with black bold text for languages
    symbol_left: "space"                # Space before the language
    symbol_right: "space"               # Space after the language
  title:
    ansi: "white,bold"                  # Bold white text for titles
    symbol_left: ""
    symbol_right: ""
  Easy:
    ansi: "green,bold"                  # Bold green text for Easy difficulty
    symbol_left: "bracket_left"         # Left bracket before difficulty
    symbol_right: "bracket_right"       # Right bracket after difficulty
  Medium:
    ansi: "orange,bold"                 # Bold orange text for Medium difficulty
    symbol_left: "bracket_left"
    symbol_right: "bracket_right"
  Hard:
    ansi: "red,bold"                     # Bold red text for Hard difficulty
    symbol_left: "bracket_left"
    symbol_right: "bracket_right"
  example_title:
    ansi: "bold"                        # Bold text for example titles
    symbol_left: ""
    symbol_right: ""
  example_input_string:
    ansi: "bold"                        # Bold text for "Input" label
    symbol_left: ""
    symbol_right: ""
  example_output_string:
    ansi: "bold"                        # Bold text for "Output" label
    symbol_left: ""
    symbol_right: ""
  example_explanation_string:
    ansi: "bold"                        # Bold text for "Explanation" label
    symbol_left: ""
    symbol_right: ""
  example_input_data:
    ansi: "gray"                        # Gray text for input data
    symbol_left: ""
    symbol_right: ""
  example_output_data:
    ansi: "gray"                        # Gray text for output data
    symbol_left: ""
    symbol_right: ""
  example_explanation_data:
    ansi: "gray"                        # Gray text for explanation data
    symbol_left: ""
    symbol_right: ""
  constraints_string:
    ansi: "bold"                        # Bold text for "Constraints" label
    symbol_left: ""
    symbol_right: ""

STATS_FORMATTER:
  # Mappings for styling user statistics and activity calendar
  EASY:
    ansi: "green"                       # Green color for Easy solved problems
    symbol_left: ""
    symbol_right: ""
  MEDIUM:
    ansi: "orange"                      # Orange color for Medium solved problems
    symbol_left: ""
    symbol_right: ""
  HARD:
    ansi: "red"                         # Red color for Hard solved problems
    symbol_left: ""
    symbol_right: ""
  CALENDAR_TIER0:
    ansi: "gray"                        # Gray color for lowest tier in calendar
    symbol_left: ""
    symbol_right: ""
  CALENDAR_TIER1:
    ansi: "orange,bold"                 # Bold orange color for higher tier in calendar
    symbol_left: ""
    symbol_right: ""
  filled_square:
    ansi: ""                            # Default color for filled squares
    symbol_left: "filled_square"        # Filled square symbol
    symbol_right: ""
  empty_square:
    ansi: ""                            # Default color for empty squares
    symbol_left: "empty_square"         # Empty square symbol
    symbol_right: ""
  field:
    ansi: "white,bold"                  # Bold white text for statistical fields
    symbol_left: ""
    symbol_right: ""
"""
