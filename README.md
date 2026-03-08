
# Leetcode CLI 🚀

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A highly customizable command-line interface for seamless interaction with Leetcode. Manage problems, test solutions, and track progress - all from your terminal!


## Table of Contents 📖
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Theming](#theming)
- [Command Reference](#command-reference)
- [Contributing](#contributing)
- [License](#license)

## Features ✨

- **Comprehensive Problem Management**
  - List problems with filters (difficulty, tags, pagination)
  - View detailed problem statements with examples and constraints
  - Random problem selection with custom filters

- **Solution Development**
  - Auto-generated solution files with official code snippets
  - Local testing against Leetcode's example cases
  - Direct solution submission to Leetcode

- **User Analytics**
  - Submission statistics and acceptance rates
  - Daily submission calendar visualization

- **Customization**
  - Theme support with separate color, symbol, and style definitions
  - Configurable section spacing and layout via theme files
  - Raw style mode (`-r`) to reveal theme keys for easy customization
  - Configurable default language and user preferences

- **Developer Experience**
  - Verbose logging (`-v`) for debugging API calls and internal state
  - Pre-commit hooks with Ruff linting/formatting and conventional commits

## Installation ⚙️

### Prerequisites
- Python 3.11+
- pip package manager

### Setup
```bash
# Clone repository
git clone https://github.com/michal-pielka/leetcode_cli
cd leetcode-cli

# Install as global package
pip install .
```

## Quick Start 🚦

https://github.com/user-attachments/assets/c7b50293-035b-40bd-97f2-1e33701daafa

1. **Initialize Configuration**
```bash
leetcode config cookie YOUR_LEETCODE_SESSION_COOKIE
leetcode config username YOUR_LEETCODE_USERNAME
leetcode config language python
```

2. **Basic Workflow**
```bash
# Find a medium difficulty array problem
leetcode list --difficulty MEDIUM --tag array

# View problem details
leetcode show 15    # Using ID
leetcode show two-sum   # Using title slug

# Create solution file
leetcode create    # Creates last seen problem solution file for default language
leetcode create 1    # Creates two-sum [1] problem solution file for default language
leetcode create two-sum    # Creates two-sum [1] problem solution file for default language
leetcode create .cpp    # Creates last seen problem solution file for C++

# Test solution
leetcode test 1.two-sum.py

# Submit solution
leetcode submit 1.two-sum.py
```

## Configuration ⚙️

Configuration files are stored in `~/.leetcode/` (Linux/macOS) or `%APPDATA%/.leetcode` (Windows).

### Key Configuration Options
| Key       | Description                                  | Example Value              |
|-----------|----------------------------------------------|----------------------------|
| cookie    | Leetcode session cookie (required)           | abc123def456ghi789jkl0     |
| username  | Leetcode username for stats                  | sample_username            |
| language  | Default programming language                 | python                     |
| theme     | Output color theme                           | gruvbox                    |

**Security Note:** Never share your Leetcode session cookie.

### Global Flags

These flags are available on every command:

| Flag              | Description                                        |
|-------------------|----------------------------------------------------|
| `-v`, `--verbose` | Enable verbose logging (debug-level) to stderr.    |
| `-h`, `--help`    | Show help for any command.                         |

### Formatting config

This CLI allows you to control what information is displayed when you **show**, **test**, or **submit** problems. You can enable or disable specific sections of the output by editing the `formatting_config.yaml` file found in your `~/.leetcode/` folder. The file is split into top-level keys (`interpretation`, `submission`, `problem_show`) corresponding to different CLI actions.

For example, when you **test** your solution (`leetcode test <FILEPATH>`), the CLI references the `interpretation` section to decide whether to display the language, testcases, or error messages. Similarly, when you **submit** a solution (`leetcode submit <FILEPATH>`), it looks at the `submission` section. When you **show** or **random** a problem, it uses the `problem_show` section to determine which parts of the problem statement to display (title, tags, examples, etc.).

Here's a simplified preview of some of the available options:

| **Category**        | **Option**                      | **Default Value** | **Description**                                                       |
|---------------------|---------------------------------|-------------------|-----------------------------------------------------------------------|
| **interpretation**  | `show_language`                 | true             | Show the programming language used in test results.                   |
|                     | `show_testcases`                | true             | Show the testcases used for the test code action.                      |
|                     | `...`          |        ...       |   ...                 ||
| **submission**      | `show_language`                 | true             | Show the programming language in submission results.                  |
|                     | `show_testcases`                | true             | If submission fails, display the testcases that caused the error.     |
|                     | `...`           | ...             | ...                                    |
| **problem_show**    | `show_title`                    | true             | Display the problem's title and difficulty.                           |
|                     | `show_tags`                     | true             | Show the problem's topic tags.                                        |
|                     | `...`                    | ...             | ...                        |

You can edit these defaults to tailor your experience. For example, if you find the error messages too verbose, set `show_detailed_error_messages: false` in the `interpretation` or `submission` sections.



## Theming 🎨

https://github.com/user-attachments/assets/c491c334-d6fa-4783-918b-28e6c1c8df8c

The CLI uses a theming system built around three YAML files per theme:

1. **ansi_codes.yaml** — Defines named ANSI escape codes (colors and text styles like `bold`, `italic`, or RGB values).
2. **symbols.yaml** — Defines named symbols (e.g., `checkmark`, `cross`, `square`) used as icons.
3. **styles.yaml** — Maps semantic elements to a `style` (comma-separated names from `ansi_codes.yaml`) and an `icon` (a name from `symbols.yaml`). Also contains a `layout` section for output formatting options like `section_spacing`.

### Discovering Theme Keys

Every command that produces styled output supports `-r`/`--raw-style`. Instead of applying colors, it prints the theme key that controls each element:

```bash
leetcode show two-sum -r
```

This outputs labels like `[text.title]`, `[difficulty.easy]`, `[status.accepted]` inline with the content, so you know exactly which entry in `styles.yaml` to edit.

### Creating a Custom Theme

1. **Create a folder** under `~/.leetcode/themes/` named after your theme, e.g. `~/.leetcode/themes/mycooltheme`.

2. **Add the three YAML files** inside it: `ansi_codes.yaml`, `symbols.yaml`, `styles.yaml`.

3. **Define colors** in `ansi_codes.yaml`:

```yaml
ANSI_CODES:
  green: "\u001b[38;2;80;250;123m"
  red:   "\u001b[38;2;255;85;85m"
  bold:  "\u001b[1m"
```

4. **Define symbols** in `symbols.yaml`:

```yaml
SYMBOLS:
  checkmark: "✔"
  cross: "✘"
  dot: "•"
```

5. **Define styles** in `styles.yaml`, mapping semantic elements to colors and icons:

```yaml
status:
  accepted:      { style: "green,bold", icon: "checkmark" }
  wrong_answer:  { style: "red,bold",   icon: "cross" }

difficulty:
  easy:   { style: "green,bold",   icon: "" }
  medium: { style: "yellow,bold",  icon: "" }
  hard:   { style: "red,bold",     icon: "" }

text:
  title:       { style: "white,bold",  icon: "" }
  description: { style: "white",       icon: "" }

layout:
  section_spacing: 2
```

The `layout.section_spacing` value controls the number of blank lines between sections in commands like `show` and `random`.

6. **Activate your theme:**

```bash
leetcode theme mycooltheme
```

### Important Notes

- All keys referenced by the CLI must be defined in `styles.yaml`. Missing keys will raise an error at render time.
- `ansi_codes.yaml` must have an `ANSI_CODES` top-level key; `symbols.yaml` must have a `SYMBOLS` top-level key.
- Revert to the built-in theme at any time:

```bash
leetcode theme default
```







## Command Reference 📚
### Full Command List

| Command               | Description                                                         |
|-----------------------|---------------------------------------------------------------------|
| **`list`**            | Display a paginated list of problems, optionally filtered.          |
| **`show`**            | Show details for a specific problem by ID or slug.                  |
| **`random`**          | Show a random problem, optionally filtered by difficulty and tags.  |
| **`create`**          | Create a new solution file from a given ID/slug with starter code.  |
| **`test`**            | Test your local solution file against example testcases.            |
| **`submit`**          | Submit your local solution file to LeetCode.                        |
| **`stats`**           | View your LeetCode stats and calendar.                              |
| **`config`**          | Set or display configuration options (cookie, username, language).  |
| **`theme`**           | Switch or list available color-symbol themes.                       |
| **`download-problems`** | Cache entire problem metadata locally.                           |

Use `leetcode <COMMAND> --help` for more details or additional flags on each command.

### Individual commands

### `list`
```bash
leetcode list [--difficulty DIFFICULTY] [--tag TAG] [--limit LIMIT] [--page PAGE] [-r]
```
- **Description:** Lists problems from the Leetcode problemset.
- **Options:**
  - `--difficulty` (optional): Filter by `EASY`, `MEDIUM`, or `HARD`.
  - `--tag` (optional, repeatable): Filter by specific tag(s) like `array`, `binary-search`.
  - `--limit` (default: 50): Number of problems per page.
  - `--page` (default: 1): Page number to display.
  - `-r`, `--raw-style`: Show theme style keys instead of colors.







### `show`
```bash
leetcode show <IDENTIFIER> [--include SECTIONS...] [-r]
```
- **Description:** Displays detailed information for a specific problem.
- **Parameters:**
  - `<IDENTIFIER>`: Either a **numeric ID** (frontend ID) or a **title slug**.
- **Options:**
  - `--include` (optional, repeatable): Override default display sections (e.g., `title`, `tags`, `langs`, `description`, `examples`, `constraints`).
  - `-r`, `--raw-style`: Show theme style keys instead of colors.







### `random`
```bash
leetcode random [--difficulty DIFFICULTY] [--tag TAG] [--include SECTIONS...] [-r]
```
- **Description:** Shows a random problem, optionally filtered by difficulty and/or tag(s).
- **Options:**
  - `--difficulty` (optional): Filter by `EASY`, `MEDIUM`, or `HARD`.
  - `--tag` (optional, repeatable): Filter by specific tag(s).
  - `--include` (optional, repeatable): Override default display sections (as in `show`).
  - `-r`, `--raw-style`: Show theme style keys instead of colors.







### `create`
```bash
leetcode create <IDENTIFIER>
```
- **Description:** Creates a local solution file with a starter code snippet for a given problem.
- **Parameters:**
  - `<IDENTIFIER>` can be:
    - **Omitted** (uses last shown problem + default language).
    - A numeric **ID** (e.g., `1`).
    - A **slug** (e.g., `two-sum`).
    - Any of the above **plus** a file extension (e.g., `two-sum.cpp`).
- **Usage Examples:**
  - `leetcode create`
  - `leetcode create 1`
  - `leetcode create two-sum.cpp`
  - `leetcode create 1.two-sum.py`







### `test`
```bash
leetcode test <FILEPATH> [--include SECTIONS...] [-r]
```
- **Description:** Tests a local solution file against the problem's built-in example testcases.
- **Parameters:**
  - `<FILEPATH>`: Must follow the format `id.title_slug.file_extension`, for example `1.two-sum.py`.
- **Options:**
  - `--include` (optional, repeatable): Override default display sections.
  - `-r`, `--raw-style`: Show theme style keys instead of colors.
- **Notes:** Displays test results (passed/failed testcases, output, errors, etc.) according to your formatting config.







### `submit`
```bash
leetcode submit <FILEPATH> [--include SECTIONS...] [-r]
```
- **Description:** Submits a local solution file to LeetCode and shows the real-time result.
- **Parameters:**
  - `<FILEPATH>`: Must follow the format `id.title_slug.file_extension`, for example `15.3sum.cpp`.
- **Options:**
  - `--include` (optional, repeatable): Override default display sections.
  - `-r`, `--raw-style`: Show theme style keys instead of colors.







### `stats`
```bash
leetcode stats [USERNAME] [--include SECTIONS...] [-r]
```
- **Description:** Fetches and displays your LeetCode profile statistics (e.g., number of solved problems) and optional submission calendar.
- **Parameters:**
  - `[USERNAME]`: If omitted, uses the username from config.
- **Options:**
  - `--include` (optional, repeatable): Choose sections to display (e.g., `stats`, `calendar`).
  - `-r`, `--raw-style`: Show theme style keys instead of colors.







### `config`
```bash
leetcode config [KEY] [VALUE]
```
- **Description:** Manages global CLI settings such as your LeetCode session cookie, default username, or default language.
- **Usage Examples:**
  - `leetcode config` — lists all current config values.
  - `leetcode config cookie <SESSION_COOKIE>`
  - `leetcode config username <USERNAME>`
  - `leetcode config language python`







### `theme`
```bash
leetcode theme [THEME_NAME]
```
- **Description:** Lists available themes or sets a new theme for colored output and symbols.
- **Parameters:**
  - `[THEME_NAME]`: Name of the theme folder under `~/.leetcode/themes`.







### `download-problems`
```bash
leetcode download-problems
```
- **Description:** Caches problem metadata locally (IDs, slugs, etc.) so that commands like `show` or `create` work offline or faster.
- **Notes:** The metadata is stored in `~/.leetcode/problems_metadata.json`.







## Contributing 🤝

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note:** This is an unofficial tool not affiliated with LeetCode. Use at your own discretion.
