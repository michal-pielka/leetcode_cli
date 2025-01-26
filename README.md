

# LeetCode CLI 🚀

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A highly customizable command-line interface for seamless interaction with Leetcode. Manage problems, test solutions, and track progress - all from your terminal!


## Table of Contents 📖
- [Features](#features-✨)
- [Installation](#installation-⚙️)
- [Quick Start](#quick-start-🚦)
- [Configuration](#configuration-⚙️)
- [Theming](#theming-🎨)
- [Command Reference](#command-reference-📚)
- [Contributing](#contributing-🤝)
- [License](#license-📄)

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
| cookie    | LeetCode session cookie (required)           | abc123def456ghi789jkl0     |
| username  | LeetCode username for stats                  | sample_username            |
| language  | Default programming language                 | python                     |
| theme     | Output color theme                           | gruvbox                       |

**Security Note:** Never share your Leetcode session cookie. [Learn how to retrieve your cookie securely](https://leetcode.com/discuss/general-discussion/1604748/using-leetcode-api-authentication-cookies).

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

By combining the **formatting config** and the **theming** system, you can customize how and what the CLI displays to perfectly suit your workflow.


## Command Reference 📚

### `list`
```bash
leetcode list [--difficulty DIFFICULTY] [--tag TAG] [--limit LIMIT] [--page PAGE]
```
- **Filters:**
  - `--difficulty`: Easy/Medium/Hard
  - `--tag`: Problem category (e.g., array, binary-search)
  - `--limit`: Results per page (default: 50)
  - `--page`: Page number (default: 1)

### `show`
```bash
leetcode show <IDENTIFIER> [--include CONTENT_SECTIONS]
```
- **Identifier:** Question ID or title slug
- **Sections:** description, examples, constraints, tags

### `create`
```bash
leetcode create [IDENTIFIER]
```
- Generates solution file with official code template
- Uses configured language if not specified

### `test`
```bash
leetcode test <FILEPATH>
```
- Validates solution against LeetCode's test cases

### `submit`
```bash
leetcode submit <FILEPATH>
```
- Submits solution and displays real-time status

### Full Command List
| Command               | Description                                   |
|-----------------------|-----------------------------------------------|
| `list`                | Display problemset                            |
| `show [IDENTIFIER]`   | Display specified problem's description       |
| `random`              | Display random problem's description          |
| `create [IDENTIFIER]` | Create specified problem's solution file      |
| `test [FILEPATH]`     | Test solution file against leetcode testcases |
| `submit [FILEPATH]`   | Submit solution file to leetcode              |
| `stats [USERNAME]`    | Display user statistics and calendar          |
| `config [KEY] [VALUE]`| Manage configuration settings                 |
| `theme [THEME_NAME]`  | Select a color-symbol theme                   |
| `download-problems`   | Cache problem metadata                        |

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
