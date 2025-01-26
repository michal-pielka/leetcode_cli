# LeetCode CLI 🚀

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A highly customizable command-line interface for seamless interaction with LeetCode. Manage problems, test solutions, and track progress - all from your terminal.

## Features ✨

- **Comprehensive Problem Management**
  - List problems with filters (difficulty, tags, pagination)
  - View detailed problem statements with examples and constraints
  - Random problem selection with custom filters

- **Solution Development**
  - Auto-generated solution files with official code snippets
  - Local testing against LeetCode's example cases
  - Direct solution submission to leetcode

- **User Analytics**
  - Submission statistics and acceptance rates
  - Daily submission calendar visualization

- **Customization**
  - Theme support for output styling
  - Configurable default language and user preferences

## Table of Contents 📖
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Command Reference](#command-reference)
- [Contributing](#contributing)
- [License](#license)

## Installation ⚙️

### Prerequisites
- Python 3.7+
- pip package manager

### Setup
```bash
# Clone repository
git clone https://github.com/michal-pielka/leetcode_cli
cd leetcode-cli

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

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
leetcode test 15_3sum.py

# Submit solution
leetcode submit 15_3sum.py
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

**Security Note:** Never share your LeetCode session cookie. [Learn how to retrieve your cookie securely](https://leetcode.com/discuss/general-discussion/1604748/using-leetcode-api-authentication-cookies).

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
```
