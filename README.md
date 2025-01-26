
# Leetcode CLI 🚀

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
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
  - Theme support for output styling
  - Configurable default language and user preferences

## Installation ⚙️

### Prerequisites
- Python 3.7+
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
| theme     | Output color theme                           | gruvbox                       |

**Security Note:** Never share your Leetcode session cookie.

### Formatting config

This CLI allows you to control what information is displayed when you **show**, **test**, or **submit** problems. You can enable or disable specific sections of the output by editing the `formatting_config.yaml` file found in your `~/.leetcode/` folder. The file is split into top-level keys (`interpretation`, `submission`, `problem_show`) corresponding to different CLI actions.

For example, when you **test** your solution (`leetcode test <FILEPATH>`), the CLI references the `interpretation` section to decide whether to display the language, testcases, or error messages. Similarly, when you **submit** a solution (`leetcode submit <FILEPATH>`), it looks at the `submission` section. When you **show** or **random** a problem, it uses the `problem_show` section to determine which parts of the problem statement to display (title, tags, examples, etc.). 

Here’s a simplified preview of some of the available options:

| **Category**        | **Option**                      | **Default Value** | **Description**                                                       |
|---------------------|---------------------------------|-------------------|-----------------------------------------------------------------------|
| **interpretation**  | `show_language`                 | true             | Show the programming language used in test results.                   |
|                     | `show_testcases`                | true             | Show the testcases used for the test code action.                      |
|                     | `...`          |        ...       |   ...                 ||
| **submission**      | `show_language`                 | true             | Show the programming language in submission results.                  |
|                     | `show_testcases`                | true             | If submission fails, display the testcases that caused the error.     |
|                     | `...`           | ...             | ...                                    |
| **problem_show**    | `show_title`                    | true             | Display the problem’s title and difficulty.                           |
|                     | `show_tags`                     | true             | Show the problem’s topic tags.                                        |
|                     | `...`                    | ...             | ...                        |

You can edit these defaults to tailor your experience. For example, if you find the error messages too verbose, set `show_detailed_error_messages: false` in the `interpretation` or `submission` sections.



https://github.com/user-attachments/assets/081c2c82-4a40-4217-8aa5-3510e0dd8c7c





## Theming 🎨

The CLI uses a theming system to style its output with colors, symbols, and prefixes/suffixes. A theme is comprised of three YAML files:

1. **ansi_codes.yaml** – Defines your ANSI color codes and text styles (e.g., `bold`, `italic`, `underline`, or RGB color codes).
2. **symbols.yaml** – Defines textual symbols (e.g., checkmarks, crosses, squares) used in CLI outputs.
3. **mappings.yaml** – Maps each CLI “key” or “status” (e.g., `status_accepted`, `difficulty_easy`) to a combination of styles and symbols.

### Creating a Custom Theme

To create your own theme:

1. **Create a folder** under `~/.leetcode/themes/` named after your theme. For example: `~/.leetcode/themes/mycooltheme`.

2. **Add your YAML files** inside that folder:
   - `ansi_codes.yaml`  
   - `symbols.yaml`  
   - `mappings.yaml`  

3. **Define your styles** in `ansi_codes.yaml`. For example:
   ```yaml
   ANSI_CODES:
     green: "\u001b[38;2;80;250;123m"
     red:   "\u001b[38;2;255;85;85m"
     bold:  "\u001b[1m"
     # etc...
   ```

4. **Define your symbols** in `symbols.yaml`. For example:
   ```yaml
   SYMBOLS:
     checkmark: "✔"
     cross: "✘"
     dot: "•"
     # etc...
   ```

5. **Map them** in `mappings.yaml` to CLI concepts, for example:
   ```yaml
   INTERPRETATION:
     status_accepted:
       style: "green,bold"
       prefix: "checkmark,space"
       suffix: ""
     # more mappings...
   SUBMISSION:
     # define how you want accepted/wrong-answer to look
     status_accepted:
       style: "green,bold"
       prefix: "checkmark,space"
       suffix: ""
     status_wrong_answer:
       style: "red,bold"
       prefix: "cross,space"
       suffix: ""
     # etc...
   ```

6. **Set your theme** by running:
   ```bash
   leetcode theme mycooltheme
   ```
   and the CLI will re-load all YAML files from your new theme folder. 

### Important Notes

- Be sure to define **all keys** in `mappings.yaml`. If you omit something like `status_accepted`, it will throw an error when encountered.  
- If you only want to override a few symbols, you still must define or copy the required sections (`INTERPRETATION`, `SUBMISSION`, `PROBLEMSET`, etc.) so the CLI can find every key it needs.
- The **`ansi_codes.yaml`** must have an `ANSI_CODES` top-level key. Similarly, **`symbols.yaml`** must have a `SYMBOLS` top-level key.  
- You can always revert to the built-in `default` theme using:
  ```bash
  leetcode theme default
  ```



https://github.com/user-attachments/assets/c3395e70-38ae-4eb6-8999-8e281625fb4b





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
| **`download-problems`** | Cache entire problem metadata locally.                          
|
Use `leetcode <COMMAND> --help` for more details or additional flags on each command.

### Individual commands

### `list`
```bash
leetcode list [--difficulty DIFFICULTY] [--tag TAG] [--limit LIMIT] [--page PAGE]
```
- **Description:** Lists problems from the Leetcode problemset.
- **Options:**
  - `--difficulty` (optional): Filter by `EASY`, `MEDIUM`, or `HARD`.
  - `--tag` (optional, repeatable): Filter by specific tag(s) like `array`, `binary-search`.
  - `--limit` (default: 50): Number of problems per page.
  - `--page` (default: 1): Page number to display.




https://github.com/user-attachments/assets/b7f709e9-44d9-4482-9a17-2cc856e226c3




### `show`
```bash
leetcode show <IDENTIFIER> [--include SECTIONS...]
```
- **Description:** Displays detailed information for a specific problem.
- **Parameters:**
  - `<IDENTIFIER>`: Either a **numeric ID** (frontend ID) or a **title slug**.
- **Options:**
  - `--include` (optional, repeatable): Override default display sections (e.g., `title`, `tags`, `langs`, `description`, `examples`, `constraints`).




https://github.com/user-attachments/assets/28112411-0ab3-4f48-a23e-ecdbacb065de




### `random`
```bash
leetcode random [--difficulty DIFFICULTY] [--tag TAG] [--include SECTIONS...]
```
- **Description:** Shows a random problem, optionally filtered by difficulty and/or tag(s).
- **Options:**
  - `--difficulty` (optional): Filter by `EASY`, `MEDIUM`, or `HARD`.
  - `--tag` (optional, repeatable): Filter by specific tag(s).
  - `--include` (optional, repeatable): Override default display sections (as in `show`).




https://github.com/user-attachments/assets/d2e99784-3b3e-4585-9c0b-c046d41cfe15




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




https://github.com/user-attachments/assets/b15e8b74-f6e0-4393-bf58-617419c00b60




### `test`
```bash
leetcode test <FILEPATH>
```
- **Description:** Tests a local solution file against the problem’s built-in example testcases.
- **Parameters:**
  - `<FILEPATH>`: Must follow the format `id.title_slug.file_extension`, for example `1.two-sum.py`.
- **Notes:** Displays test results (passed/failed testcases, output, errors, etc.) according to your formatting config.




https://github.com/user-attachments/assets/fb1a0886-a697-4178-97db-dc651270d6eb




### `submit`
```bash
leetcode submit <FILEPATH>
```
- **Description:** Submits a local solution file to LeetCode and shows the real-time result.
- **Parameters:**
  - `<FILEPATH>`: Must follow the format `id.title_slug.file_extension`, for example `15.3sum.cpp`.




https://github.com/user-attachments/assets/5406ceed-a59f-46a4-936f-99ba48734f4f




### `stats`
```bash
leetcode stats [USERNAME] [--include SECTIONS...]
```
- **Description:** Fetches and displays your LeetCode profile statistics (e.g., number of solved problems) and optional submission calendar.
- **Parameters:**
  - `[USERNAME]`: If omitted, uses the username from config.
- **Options:**
  - `--include` (optional, repeatable): Choose sections to display (e.g., `stats`, `calendar`).



https://github.com/user-attachments/assets/f8a712e8-6418-4913-8841-e19338386746





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




https://github.com/user-attachments/assets/57dc61f0-ad99-485e-9213-dbe32c2b1e07




### `theme`
```bash
leetcode theme [THEME_NAME]
```
- **Description:** Lists available themes or sets a new theme for colored output and symbols.
- **Parameters:**
  - `[THEME_NAME]`: Name of the theme folder under `~/.leetcode/themes`.





https://github.com/user-attachments/assets/55ad8782-6f23-4b00-babf-b7672791c6c9



### `download-problems`
```bash
leetcode download-problems
```
- **Description:** Caches problem metadata locally (IDs, slugs, etc.) so that commands like `show` or `create` work offline or faster.
- **Notes:** The metadata is stored in `~/.leetcode/problems_metadata.json`.




https://github.com/user-attachments/assets/c869c161-eb67-4b73-bf34-7db8ee027920




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
