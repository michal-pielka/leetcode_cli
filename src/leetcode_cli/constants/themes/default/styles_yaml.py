STYLES_YAML = """# Theme styles configuration.
# Each entry maps a semantic element to a visual style.
#   "style" - comma-separated color/style names from ansi_codes.yaml (e.g. "green,bold")
#   "icon"  - a symbol name from symbols.yaml shown before the text (e.g. "checkmark")
# Layout options control spacing and formatting in the CLI output.

status:
  accepted:               { style: "green,bold",  icon: "checkmark" }
  wrong_answer:           { style: "red,bold",    icon: "cross" }
  memory_limit_exceeded:  { style: "red,bold",    icon: "cross" }
  output_limit_exceeded:  { style: "red,bold",    icon: "cross" }
  time_limit_exceeded:    { style: "red,bold",    icon: "cross" }
  runtime_error:          { style: "red,bold",    icon: "cross" }
  compile_error:          { style: "red,bold",    icon: "cross" }
  unknown:                { style: "orange,bold", icon: "cross" }
  ac:                     { style: "green",       icon: "checkmark" }
  notac:                  { style: "orange",      icon: "bullseye" }
  not_started:            { style: "" }

difficulty:
  easy:   { style: "green,bold" }
  medium: { style: "orange,bold" }
  hard:   { style: "red,bold" }

text:
  title:         { style: "white,bold" }
  heading:       { style: "white,bold" }
  label:         { style: "white" }
  value:         { style: "white" }
  description:   { style: "" }
  example_label: { style: "bold" }
  example_value: { style: "gray" }
  question_id:   { style: "white,bold" }
  ac_rate:       { style: "white" }
  tag:           { style: "cyan_bg,white,bold" }
  language:      { style: "orange_bg,black,bold" }

html:
  strong:     { style: "bold" }
  b:          { style: "bold" }
  em:         { style: "italic" }
  i:          { style: "italic" }
  u:          { style: "underline" }
  code:       { style: "gray_bg" }
  pre:        { style: "red" }
  li:         { style: "",  icon: "dot" }
  sup:        { style: "" }
  sub:        { style: "" }
  p:          { style: "" }
  br:         { style: "" }
  ul:         { style: "" }
  ol:         { style: "" }
  a:          { style: "" }
  span:       { style: "" }
  div:        { style: "" }
  table:      { style: "" }
  img:        { style: "" }
  blockquote: { style: "" }
  ptable:     { style: "" }
  font:       { style: "" }
  var:        { style: "" }
  meta:       { style: "" }
  style:      { style: "" }

calendar:
  least_submissions: { style: "dark_green",   icon: "filled_square" }
  most_submissions:  { style: "bright_green" }

paid:
  paid_only:     { style: "red", icon: "star" }
  not_paid_only: { style: "" }

layout:
  section_spacing: 2
"""
