# LeetCode CLI

A highly customizable command-line interface for interacting with LeetCode. This tool allows you to list problems, view problem details, test and submit solutions, display user stats, and more — all without leaving the terminal.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Initialization](#initialization)
4. [Configuration](#configuration)
5. [Commands](#commands)
   - [list](#list)
   - [show](#show)
   - [random](#random)
   - [create](#create)
   - [test](#test)
   - [submit](#submit)
   - [stats](#stats)
   - [theme](#theme)
   - [download-problems](#download-problems)
   - [config](#config)
6. [Placeholders for Demonstrations](#placeholders-for-demonstrations)
7. [Contributing](#contributing)
8. [License](#license)

---

## Overview

This CLI tool aims to streamline your LeetCode experience by providing a unified command-line interface. Key features include:

- **Manage** and **list** LeetCode problems with filtering (difficulty, tags).
- **View** full problem statements, examples, constraints, and tags.
- **Create** solution files pre-filled with official code snippets.
- **Test** solutions against LeetCode’s example testcases.
- **Submit** solutions directly to LeetCode.
- **View** your user statistics and daily submission calendar.
- **Customize** output formatting and theming to suit your preferences.

---

## Installation

1. Clone this repository or download the source code.
2. Make sure you have Python 3.7+ installed.
3. Install dependencies (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) If you want to use this as a global command, you can install it as a pip package using `pip install .`. For local development or usage, simply run:
   ```bash
   python cli.py --help
   ```

---

## Initialization

The CLI will ensure necessary config, theme files and directories exist in your home folder `~/.leetcode` on Linux/macOS and `~/AppData/Roaming` on Windows). 

This is done via:
```python
from leetcode_cli.init_app_files import initialize_leetcode_cli
initialize_leetcode_cli()
```
This step is automatically invoked whenever you run any `leetcode` command from the `cli.py` entry point.

---

## Configuration

Before using commands that require authentication (e.g., testing or submitting solutions), you should set your LeetCode cookie and optionally your username:

```bash
leetcode config cookie your_full_cookie
leetcode config username your_username
```

The `language` config can also be set to a default language for creating solution files:
```bash
leetcode config language python
```

These values are stored in `~/.leetcode/config.json`.

---

## Commands

Below is an overview of all the available CLI commands. For each command, you can also run `--help` to see usage details.

### list

- **Usage**:  
  ```bash
  leetcode list [--difficulty EASY|MEDIUM|HARD] [--tag TAG_NAME] [--limit 50] [--page 1]
  ```
- **Description**: Lists LeetCode problems with optional filters for difficulty, tags, pagination, etc.

<details>
<summary><strong>Video Demonstration</strong></summary>
> **Video Demonstration Placeholder**  
> *(Insert a link, screenshot, or embedded video here)*
</details>


### show

- **Usage**:  
  ```bash
  leetcode show <title_slug_or_frontend_id> [--include SECTION ...]
  ```
- **Description**: Shows detailed information for a specified problem and marks it as the "chosen_problem" in your config. You can override which sections to display via `--include`.

<details>
<summary><strong>Video Demonstration</strong></summary>
> **Video Demonstration Placeholder**  
> *(Insert a link, screenshot, or embedded video here)*
</details>


### random

- **Usage**:  
  ```bash
  leetcode random [--difficulty EASY|MEDIUM|HARD] [--tag TAG_NAME] [--include SECTION ...]
  ```
- **Description**: Shows detailed information for a random problem with optional filters for difficulty and tags. Marks that problem as the “chosen_problem” in your config. You can override which sections to display via `--include`.

<details>
<summary><strong>Video Demonstration</strong></summary>
> **Video Demonstration Placeholder**  
> *(Insert a link, screenshot, or embedded video here)*
</details>


### create

- **Usage**:  
  ```bash
  leetcode create [TITLE_SLUG_OR_ID]
  ```
- **Description**: Creates a local solution file for a given problem with official code snippets for your default language, unless provided with a different language.

<details>
<summary><strong>Video Demonstration</strong></summary>
> **Video Demonstration Placeholder**  
> *(Insert a link, screenshot, or embedded video here)*
</details>


### test

- **Usage**:  
  ```bash
  leetcode test <file_path> [--include SECTION ...]
  ```
- **Description**: Tests your solution file against the example testcases provided by LeetCode.

<details>
<summary><strong>Video Demonstration</strong></summary>
> **Video Demonstration Placeholder**  
> *(Insert a link, screenshot, or embedded video here)*
</details>


### submit

- **Usage**:  
  ```bash
  leetcode submit <file_path> [--include SECTION ...]
  ```
- **Description**: Submits your solution file directly to LeetCode and shows the submission result.


### stats

- **Usage**:  
  ```bash
  leetcode stats [USERNAME] [--include stats --include calendar]
  ```
- **Description**: Shows your overall accepted/failed counts per difficulty and a daily submission calendar.

<details>
<summary><strong>Video Demonstration</strong></summary>
> **Video Demonstration Placeholder**  
> *(Insert a link, screenshot, or embedded video here)*
</details>


<details>
<summary><strong>Video Demonstration</strong></summary>
> **Video Demonstration Placeholder**  
> *(Insert a link, screenshot, or embedded video here)*
</details>


### theme

- **Usage**:  
  ```bash
  leetcode theme [theme_name]
  ```
- **Description**: Lists available themes (if no argument is given) or sets a new theme.

<details>
<summary><strong>9. theme Command</strong></summary>

**Usage**: `leetcode theme [theme_name]`

> **Video Demonstration Placeholder**  
> *(Insert a link, screenshot, or embedded video here)*
</details>


### download-problems

- **Usage**:  
  ```bash
  leetcode download-problems
  ```
- **Description**: Downloads a full JSON metadata listing of all LeetCode problems and saves it locally, enabling references by problem ID.

### config

- **Usage**:  
  ```bash
  leetcode config               # show all config key-value pairs
  leetcode config <key> <value> # set a config key
  ```
- **Description**: Manages your `cookie`, `username`, and `language` fields in `~/.leetcode/config.json`.

<details>
<summary><strong>1. config Command</strong></summary>

**Usage**: `leetcode config <key> <value>` or just `leetcode config`

> **Video Demonstration Placeholder**  
> *(Insert a link, screenshot, or embedded video here)*
</details>

---

## Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

---

## License

This project is provided under the [MIT License](LICENSE).  
Feel free to use, modify, and distribute this software in accordance with the license terms.
