```markdown
# LeetCode CLI 🚀

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-grade command-line interface for seamless interaction with LeetCode. Manage problems, test solutions, and track progress - all from your terminal.

## Features ✨

- **Comprehensive Problem Management**
  - List problems with filters (difficulty, tags, pagination)
  - View detailed problem statements with examples and constraints
  - Random problem selection with custom filters
- **Solution Development**
  - Auto-generated solution files with official code snippets
  - Local testing against LeetCode's example cases
  - Direct solution submission to LeetCode
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
git clone https://github.com/yourusername/leetcode-cli.git
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
leetcode show 15   # Using frontend ID
leetcode show "3sum"  # Using title slug

# Create solution file
leetcode create 15 --language python

# Test solution
leetcode test solutions/15_3sum.py

# Submit solution
leetcode submit solutions/15_3sum.py
```

## Configuration ⚙️

Configuration files are stored in `~/.leetcode/` (Linux/macOS) or `%APPDATA%/.leetcode` (Windows).

### Key Configuration Options
| Key       | Description                                  | Example Value              |
|-----------|----------------------------------------------|----------------------------|
| cookie    | LeetCode session cookie (required)          | abc123def456ghi789jkl0     |
| username  | LeetCode username for stats                 | code_champion              |
| language  | Default programming language                | python3                    |
| theme     | Output color theme                          | dark                       |

**Security Note:** Never share your LeetCode session cookie. [Learn how to retrieve your cookie securely](https://leetcode.com/discuss/general-discussion/1604748/using-leetcode-api-authentication-cookies).

## Command Reference 📚

### `list`
```bash
leetcode list [--difficulty DIFFICULTY] [--tag TAG] [--limit LIMIT] [--page PAGE]
```
- **Filters:**
  - `--difficulty`: Easy/Medium/Hard
  - `--tag`: Problem category (e.g., array, tree)
  - `--limit`: Results per page (default: 50)
  - `--page`: Pagination offset

### `show`
```bash
leetcode show <IDENTIFIER> [--include CONTENT_SECTIONS]
```
- **Identifier:** Frontend ID or title slug
- **Sections:** description, examples, constraints, tags

### `create`
```bash
leetcode create [IDENTIFIER] [--language LANG]
```
- Generates solution file with official code template
- Uses configured language if not specified

### `test`
```bash
leetcode test <FILEPATH> [--verbose]
```
- Validates solution against LeetCode's test cases
- `--verbose`: Show detailed execution results

### `submit`
```bash
leetcode submit <FILEPATH> [--watch]
```
- Submits solution and displays real-time status
- `--watch`: Poll for submission results continuously

### Full Command List
| Command               | Description                                  |
|-----------------------|----------------------------------------------|
| `stats [USERNAME]`    | Display user statistics and calendar         |
| `theme [THEME_NAME]`  | Configure output color scheme                |
| `download-problems`   | Cache complete problem metadata              |
| `config [KEY] [VALUE]`| Manage configuration settings                |

## Contributing 🤝

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Development Setup:**
```bash
# Install development dependencies
pip install -r dev-requirements.txt

# Run tests
python -m pytest tests/
```

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note:** This is an unofficial tool not affiliated with LeetCode. Use at your own discretion.
```
