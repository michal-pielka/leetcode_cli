ANSI_RESET = "\033[0m"       # Reset all styles

ANSI_CODES = {
    # Foreground colors
    "GREEN"         : "\033[32m",                        # Standard green
    "ORANGE"        : "\033[38;5;208m",                 # 256-color mode orange
    "RED"           : "\033[31m",                       # Standard red
    "GRAY"          : "\033[90m",                       # Dim gray
    "CYAN"          : "\033[96m",                       # Bright cyan
    "WHITE"         : "\033[38;2;255;255;255m",         # RGB white
    "BLACK"         : "\033[38;2;0;0;0m",               # RGB black

    # Custom shades of green for stats
    "GREEN1"        : "\033[38;2;1;155;1m",             # Darkest green
    "GREEN2"        : "\033[38;2;16;175;16m",
    "GREEN3"        : "\033[38;2;33;195;33m",
    "GREEN4"        : "\033[38;2;61;215;61m",
    "GREEN5"        : "\033[38;2;82;235;82m",
    "GREEN6"        : "\033[38;2;100;255;100m",         # Lightest green

    # Background colors
    "GRAY_BG"       : "\033[100m",                      # Dim gray background
    "GREEN_BG"      : "\033[42m",                       # Standard green background
    "ORANGE_BG"     : "\033[48;5;208m",                 # 256-color mode orange background
    "BABY_BLUE_BG"  : "\033[48;2;66;205;245m",         # RGB baby blue background
    "RED_BG"        : "\033[41m",                       # Standard red background
    "ORANGE_BG"     : "\033[48;2;245;158;66]",

    # Text styles
    "BOLD"          : "\033[1m",                        # Bold text
    "ITALIC"        : "\033[3m",                        # Italic text (not supported in all terminals)
    "UNDERLINE"     : "\033[4m",                        # Underlined text
}
