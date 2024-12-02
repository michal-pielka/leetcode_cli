from bs4 import BeautifulSoup, NavigableString, Tag
import re
import logging

from ..graphics.escape_sequences import ANSI_CODES, ANSI_RESET
from ..graphics.symbols import SYMBOLS

logger = logging.getLogger(__name__)

class LeetCodeProblemParserError(Exception):
    """Custom exception for LeetCodeProblemParser errors."""
    pass

class LeetCodePaidOnlyProblemError(Exception):
    """Custom exception for paid-only problems when content is inaccessible."""
    pass

class LeetCodeProblemParser:
    HTML_TO_ANSI = {
        "strong": ANSI_CODES["BOLD"],
        "b": ANSI_CODES["BOLD"],
        "em": ANSI_CODES["ITALIC"],
        "i": ANSI_CODES["ITALIC"],
        "u": ANSI_CODES["UNDERLINE"],
        "code": ANSI_CODES["GRAY_BG"],
        "pre": ANSI_CODES["RED"],
        "tag": ANSI_CODES["BABY_BLUE_BG"] + ANSI_CODES["WHITE"] + ANSI_CODES["BOLD"],
        "language": ANSI_CODES["ORANGE_BG"] + ANSI_CODES["BLACK"] + ANSI_CODES["BOLD"],
        "title": ANSI_CODES["BOLD"],
        "example_title": ANSI_CODES["BOLD"],
        "example_input_string": ANSI_CODES["BOLD"],
        "example_output_string": ANSI_CODES["BOLD"],
        "example_explanation_string": ANSI_CODES["BOLD"],
        "example_input_data": ANSI_CODES["GRAY"],
        "example_output_data": ANSI_CODES["GRAY"],
        "example_explanation_data": ANSI_CODES["GRAY"],
        "constraints_string": ANSI_CODES["BOLD"],
        "Easy": ANSI_CODES["GREEN_BG"],
        "Medium": ANSI_CODES["ORANGE_BG"],
        "Hard": ANSI_CODES["RED_BG"],
    }

    HTML_TO_SYMBOL = {
        "sup": SYMBOLS["CARET"],
        "li": SYMBOLS["DOT"] + " ",
    }

    def __init__(self, metadata: dict):
        """
        Initializes the parser with problem metadata.

        Args:
            metadata (dict): The raw problem metadata fetched from LeetCode API.

        Raises:
            LeetCodeProblemParserError: If metadata is invalid or missing.
            LeetCodePaidOnlyProblemError: If the problem is paid-only and content is inaccessible.
        """
        if not metadata or not isinstance(metadata, dict):
            logger.error("Metadata must be a non-empty dictionary.")
            raise LeetCodeProblemParserError("Metadata must be a non-empty dictionary.")

        self.metadata = metadata
        self.question_data = self._extract_question_data()
        self.is_paid_only = self.question_data.get("isPaidOnly", False)
        self.question_html_content = self.question_data.get("content", "")

        # Check if the problem is paid-only and content is inaccessible
        if self.is_paid_only and not self.question_html_content:
            logger.warning("This is a paid-only problem and the content is inaccessible.")
            raise LeetCodePaidOnlyProblemError("This is a paid-only problem and the content is inaccessible.")

        # Extracted attributes
        self.question_id = self.question_data.get("frontendQuestionId", "")
        self.question_title = self.question_data.get("title", "")
        self.question_description = self._extract_question_description()
        self.question_examples = self._extract_question_examples()
        self.question_constraints = self._extract_question_constraints()
        self.question_hints = self.question_data.get("hints", [])
        self.question_topic_tags = self.question_data.get("topicTags", [])
        self.question_languages = self.metadata.get("data", {}).get("submittableLanguageList", [])
        self.question_difficulty = self.question_data.get("difficulty", "")
        self.question_likes = self.question_data.get("likes", 0)
        self.question_dislikes = self.question_data.get("dislikes", 0)
        self.question_example_testcases = self.question_data.get("exampleTestcases", "")

    def _extract_question_data(self) -> dict:
        """
        Extracts question data from metadata.

        Returns:
            dict: The question data.

        Raises:
            LeetCodeProblemParserError: If required data is missing.
        """
        try:
            return self.metadata["data"]["question"]

        except KeyError as e:
            logger.error(f"Missing key in metadata: {e}")
            raise LeetCodeProblemParserError(f"Missing key in metadata: {e}")

    def _extract_question_description(self) -> str:
        """
        Extracts the question description from HTML content.

        Returns:
            str: The question description in HTML.
        """
        soup = BeautifulSoup(self.question_html_content, "html.parser")
        description_elements = []
        for element in soup.find_all(['p', 'ul']):
            if element.find('strong', string=re.compile(r'Example')):
                break
            description_elements.append(str(element))
        description_html = "\n".join(description_elements).strip()
        return description_html

    def _extract_question_examples(self) -> list:
        """
        Extracts examples from the question content.

        Returns:
            list: A list of example dictionaries.
        """
        soup = BeautifulSoup(self.question_html_content, "html.parser")
        examples = []
        example_headers = soup.find_all('strong', string=re.compile(r'Example \d+'))
        for header in example_headers:
            example = self._parse_example_section(header)
            if example:
                examples.append(example)
        return examples

    def _parse_example_section(self, header) -> dict:
        """
        Parses an example section from the HTML.

        Args:
            header (Tag): The header tag of the example.

        Returns:
            dict: A dictionary containing the example data.
        """
        example_title = header.get_text(strip=True).rstrip(':')
        pre_tag = header.find_next('pre')
        if not pre_tag:
            return None
        example_content = pre_tag.decode_contents()
        parsed_example = self._parse_example_content(example_content)
        if parsed_example:
            parsed_example['title'] = example_title
            return parsed_example
        return None

    def _parse_example_content(self, html_content: str) -> dict:
        """
        Parses the content of an example.

        Args:
            html_content (str): The HTML content of the example.

        Returns:
            dict: A dictionary containing input, output, and explanation.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        content_text = soup.get_text(separator="\n").strip()
        example_dict = {}

        # Use regular expressions to capture 'Input', 'Output', and 'Explanation' sections
        input_match = re.search(r'Input:\s*(.*?)(?:\nOutput:|\Z)', content_text, re.DOTALL)
        output_match = re.search(r'Output:\s*(.*?)(?:\nExplanation:|\Z)', content_text, re.DOTALL)
        explanation_match = re.search(r'Explanation:\s*(.*)', content_text, re.DOTALL)

        if input_match:
            example_dict['input'] = input_match.group(1).strip()
        if output_match:
            example_dict['output'] = output_match.group(1).strip()
        if explanation_match:
            example_dict['explanation'] = explanation_match.group(1).strip()
        return example_dict

    def _parse_input(self, input_str: str) -> dict:
        """
        Parses the input string of an example, correctly handling nested lists.

        Args:
            input_str (str): The input string.

        Returns:
            dict: A dictionary of input parameters.
        """
        input_dict = {}
        # Pattern to match key = value, where value can be anything until the next comma at the top level
        pattern = r'(\w+)\s*=\s*([\s\S]+?)(?:(?<=\])|(?<=\})|(?<=\")|(?<=\')|$)(?:,|$)'
        matches = re.finditer(pattern, input_str)
        for match in matches:
            key = match.group(1).strip()
            value = match.group(2).strip()
            input_dict[key] = value
        return input_dict

    def _extract_question_constraints(self) -> list:
        """
        Extracts the constraints from the question content.

        Returns:
            list: A list of constraint strings.
        """
        soup = BeautifulSoup(self.question_html_content, "html.parser")
        constraints_header = soup.find('strong', string='Constraints:')
        if not constraints_header:
            return []
        ul_tag = constraints_header.find_next('ul')
        if not ul_tag:
            return []
        constraints = [str(li) for li in ul_tag.find_all('li')]
        return constraints

    def html_to_ansi(self, html_content: str) -> str:
        """
        Converts HTML content to ANSI-formatted string.

        Args:
            html_content (str): The HTML content.

        Returns:
            str: The ANSI-formatted string.
        """
        if not html_content:
            return ""
        soup = BeautifulSoup(html_content, "html.parser")
        ansi_str = ""
        style_stack = []

        def traverse(element):
            nonlocal ansi_str
            if isinstance(element, NavigableString):
                ansi_str += element
            elif isinstance(element, Tag):
                if element.name in self.HTML_TO_SYMBOL:
                    ansi_str += self.HTML_TO_SYMBOL[element.name]
                if element.name in self.HTML_TO_ANSI:
                    ansi_code = self.HTML_TO_ANSI[element.name]
                    ansi_str += ansi_code
                    style_stack.append(ansi_code)
                if element.name in ['p', 'br', 'ul']:
                    ansi_str += '\n'
                for child in element.children:
                    traverse(child)
                if element.name in self.HTML_TO_ANSI:
                    ansi_str += ANSI_RESET
                    if style_stack:
                        style_stack.pop()

        for child in soup.children:
            traverse(child)
        return ansi_str

    def get_formatted_topic_tags(self) -> str:
        """
        Formats the topic tags.

        Returns:
            str: A formatted string of topic tags.
        """
        formatted_tags = ["Tags:"]

        for tag in self.question_topic_tags:
            tag_name = " " + tag["name"].lower() + " "
            formatted_tags.append(self.HTML_TO_ANSI["tag"] + tag_name + ANSI_RESET + " ")

        return " ".join(formatted_tags)

    def get_formatted_languages(self) -> str:
        """
        Formats the submittable languages.

        Returns:
            str: A formatted string of languages
        """
        formatted_languages = ["Languages:"]

        for language in self.question_languages:
            language_name = " " + language["name"] + " "
            formatted_language = f"{self.HTML_TO_ANSI['language']}{language_name}{ANSI_RESET}"
            formatted_languages.append(formatted_language)

        return " ".join(formatted_languages)

    def get_formatted_title(self) -> str:
        """
        Formats the question title.

        Returns:
            str: The formatted title.
        """
        difficulty_color = self.HTML_TO_ANSI.get(self.question_difficulty, "")
        title = f"[{self.question_id}] {self.question_title} {difficulty_color}[{self.question_difficulty}]{ANSI_RESET}"
        return f"{self.HTML_TO_ANSI['title']}{title}{ANSI_RESET}"

    def get_formatted_description(self) -> str:
        """
        Formats the question description.

        Returns:
            str: The formatted description.
        """
        if not self.question_description:
            return "No description available."
        return self.html_to_ansi(self.question_description)

    def _format_example(self, example: dict) -> str:
        """
        Formats a single example.

        Args:
            example (dict): The example data.

        Returns:
            str: The formatted example string.
        """
        parts = []
        parts.append(f"{self.HTML_TO_ANSI['example_title']}{example['title']}{ANSI_RESET}\n\n")
        parts.append(f"| {self.HTML_TO_ANSI['example_input_string']}Input: {ANSI_RESET}{self.HTML_TO_ANSI['example_input_data']}{example['input']}{ANSI_RESET}\n")
        parts.append(f"| {self.HTML_TO_ANSI['example_output_string']}Output: {ANSI_RESET}{self.HTML_TO_ANSI['example_output_data']}{example['output']}{ANSI_RESET}")
        if 'explanation' in example:
            explanation = example['explanation'].replace("\n", f"{ANSI_RESET}\n| {self.HTML_TO_ANSI['example_explanation_data']}")
            parts.append(f"\n| {self.HTML_TO_ANSI['example_explanation_string']}Explanation: {ANSI_RESET}{self.HTML_TO_ANSI['example_explanation_data']}{explanation}{ANSI_RESET}")
        return "".join(parts)

    def get_formatted_examples(self) -> str:
        """
        Formats all examples.

        Returns:
            str: The formatted examples.
        """
        formatted_examples = [self._format_example(example) for example in self.question_examples]
        return "\n\n".join(formatted_examples)

    def get_formatted_constraints(self) -> str:
        """
        Formats the constraints.

        Returns:
            str: The formatted constraints.
        """
        if not self.question_constraints:
            return ""
        constraints = [self.html_to_ansi(html) for html in self.question_constraints]
        constraints_str = "\n".join(constraints)
        return f"{self.HTML_TO_ANSI['constraints_string']}Constraints:{ANSI_RESET}\n\n{constraints_str}"
