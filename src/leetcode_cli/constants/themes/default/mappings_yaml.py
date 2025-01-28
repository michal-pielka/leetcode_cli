MAPPINGS_YAML = """# This file unifies style codes and symbol references under a single dictionary.
# Each category (INTERPRETATION, SUBMISSION, PROBLEMSET, PROBLEM_DESCRIPTION, STATS)
# uses more standardized keys. We still rely on the code hooking them up via an
# internal "translation" if the underlying data uses different strings.

INTERPRETATION:
  status_accepted:
    style: "green,bold"
    prefix: "checkmark,space"
    suffix: ""

  status_wrong_answer:
    style: "red,bold"
    prefix: "cross,space"
    suffix: ""

  status_memory_limit_exceeded:
    style: "red,bold"
    prefix: "cross,space"
    suffix: ""

  status_output_limit_exceeded:
    style: "red,bold"
    prefix: "cross,space"
    suffix: ""

  status_time_limit_exceeded:
    style: "red,bold"
    prefix: "cross,space"
    suffix: ""

  status_runtime_error:
    style: "red,bold"
    prefix: "cross,space"
    suffix: ""

  status_compile_error:
    style: "red,bold"
    prefix: "cross,space"
    suffix: ""

  status_unknown:
    style: "orange,bold"
    prefix: "cross,space"
    suffix: ""

  label_field:
    style: "white"
    prefix: ""
    suffix: "colon"

  value_field:
    style: "white"
    prefix: ""
    suffix: ""


SUBMISSION:
  status_accepted:
    style: "green,bold"
    prefix: "checkmark,space"
    suffix: ""

  status_wrong_answer:
    style: "red,bold"
    prefix: "cross,space"
    suffix: ""

  status_memory_limit_exceeded:
    style: "red,bold"
    prefix: "cross,space"
    suffix: ""

  status_output_limit_exceeded:
    style: "red,bold"
    prefix: "cross,space"
    suffix: ""

  status_time_limit_exceeded:
    style: "red,bold"
    prefix: "cross,space"
    suffix: ""

  status_runtime_error:
    style: "red,bold"
    prefix: "cross,space"
    suffix: ""

  status_compile_error:
    style: "red,bold"
    prefix: "cross,space"
    suffix: ""

  status_unknown:
    style: "orange,bold"
    prefix: "cross,space"
    suffix: ""

  label_field:
    style: "white"
    prefix: ""
    suffix: "colon"

  value_field:
    style: "white"
    prefix: ""
    suffix: ""


PROBLEMSET:
  text_title:
    style: "white"
    prefix: ""
    suffix: ""

  text_acceptance_rate:
    style: "white"
    prefix: "parenthesis_left"
    suffix: "percentage,parenthesis_right"

  text_question_id:
    style: "white,bold"
    prefix: "bracket_left"
    suffix: "bracket_right"

  difficulty_easy:
    style: "green,bold"
    prefix: ""
    suffix: ""

  difficulty_medium:
    style: "orange,bold"
    prefix: ""
    suffix: ""

  difficulty_hard:
    style: "red,bold"
    prefix: ""
    suffix: ""

  status_ac:
    style: "green"
    prefix: "checkmark"
    suffix: ""

  status_notac:
    style: "orange"
    prefix: "bullseye"
    suffix: ""

  status_not_started:
    style: ""
    prefix: "space"
    suffix: ""

  paid_only:
    style: "red"
    prefix: "star"
    suffix: ""

  not_paid_only:
    style: ""
    prefix: "space"
    suffix: ""


PROBLEM_DESCRIPTION:
  label_title:
    style: "white,bold"
    prefix: ""
    suffix: ""

  difficulty_easy:
    style: "green,bold"
    prefix: "bracket_left"
    suffix: "bracket_right"

  difficulty_medium:
    style: "orange,bold"
    prefix: "bracket_left"
    suffix: "bracket_right"

  difficulty_hard:
    style: "red,bold"
    prefix: "bracket_left"
    suffix: "bracket_right"

  label_tags:
    style: "white,bold"
    prefix: ""
    suffix: ""

  value_tags:
    style: "cyan_bg,white,bold"
    prefix: "space"
    suffix: "space"

  label_languages:
    style: "white,bold"
    prefix: ""
    suffix: ""

  value_languages:
    style: "orange_bg,black,bold"
    prefix: "space"
    suffix: "space"

  value_description:
    style: ""
    prefix: ""
    suffix: ""

  label_example_title:
    style: "bold"
    prefix: ""
    suffix: ""

  label_example_input:
    style: "bold"
    prefix: "pipe,space"
    suffix: "colon,space"

  label_example_output:
    style: "bold"
    prefix: "pipe,space"
    suffix: "colon,space"

  label_example_explanation:
    style: "bold"
    prefix: "pipe,space"
    suffix: "colon,space"

  value_example_input:
    style: "gray"
    prefix: ""
    suffix: ""

  value_example_output:
    style: "gray"
    prefix: ""
    suffix: ""

  value_example_explanation:
    style: "gray"
    prefix: ""
    suffix: ""

  label_constraints:
    style: "bold"
    prefix: ""
    suffix: ""

  # HTML TAGS
  html_strong:
    style: "bold"
    prefix: ""
    suffix: ""

  html_p:
    style: ""
    prefix: ""
    suffix: ""

  html_br:
    style: ""
    prefix: ""
    suffix: ""

  html_ul:
    style: ""
    prefix: ""
    suffix: ""

  html_li:
    style: ""
    prefix: "dot"
    suffix: ""

  html_sup:
    style: ""
    prefix: "caret"
    suffix: ""

  html_b:
    style: "bold"
    prefix: ""
    suffix: ""

  html_em:
    style: "italic"
    prefix: ""
    suffix: ""

  html_i:
    style: "italic"
    prefix: ""
    suffix: ""

  html_u:
    style: "underline"
    prefix: ""
    suffix: ""

  html_span:
    style: ""
    prefix: ""
    suffix: ""

  html_ol:
    style: ""
    prefix: ""
    suffix: ""

  html_table:
    style: ""
    prefix: ""
    suffix: ""

  html_img:
    style: ""
    prefix: ""
    suffix: ""

  html_a:
    style: ""
    prefix: ""
    suffix: ""

  html_sub:
    style: ""
    prefix: ""
    suffix: ""

  html_blockquote:
    style: ""
    prefix: ""
    suffix: ""

  html_ptable:
    style: ""
    prefix: ""
    suffix: ""

  html_font:
    style: ""
    prefix: ""
    suffix: ""

  html_var:
    style: ""
    prefix: ""
    suffix: ""

  html_meta:
    style: ""
    prefix: ""
    suffix: ""

  html_div:
    style: ""
    prefix: ""
    suffix: ""

  html_style:
    style: ""
    prefix: ""
    suffix: ""

  html_code:
    style: "gray_bg"
    prefix: "space"
    suffix: "space"

  html_pre:
    style: "red"
    prefix: ""
    suffix: ""


STATS_FORMATTER:
  difficulty_easy:
    style: "green"
    prefix: ""
    suffix: ""

  difficulty_medium:
    style: "orange"
    prefix: ""
    suffix: ""

  difficulty_hard:
    style: "red"
    prefix: ""
    suffix: ""

  correct_problems_easy:
    style: ""
    prefix: ""
    suffix: "space,slash"

  correct_problems_medium:
    style: ""
    prefix: ""
    suffix: "space,slash"

  correct_problems_hard:
    style: ""
    prefix: ""
    suffix: "space,slash"

  total_problems_easy:
    style: ""
    prefix: "space"
    suffix: ""

  total_problems_medium:
    style: ""
    prefix: "space"
    suffix: ""

  total_problems_hard:
    style: ""
    prefix: "space"
    suffix: ""

  beats_number_easy:
    style: ""
    prefix: "parenthesis_left"
    suffix: "percentage,parenthesis_right"

  beats_number_medium:
    style: ""
    prefix: "parenthesis_left"
    suffix: "percentage,parenthesis_right"

  beats_number_hard:
    style: ""
    prefix: "parenthesis_left"
    suffix: "percentage,parenthesis_right"

  calendar_least_submissions: 
    style: "dark_green"
    prefix: "filled_square"
    suffix: ""

  calendar_most_submissions:
    style: "bright_green"
    prefix: ""
    suffix: ""
"""
