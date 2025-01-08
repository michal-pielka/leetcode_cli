import json
from typing import Dict
from bs4 import BeautifulSoup, Tag, NavigableString

from leetcode_cli.models.problem import Problem


def parse_problem_data(json_data: Dict) -> Problem:
    """
    Parses raw JSON data of a LeetCode problem and returns a Problem instance.

    Args:
        json_data (Dict): The raw JSON data containing problem details.

    Returns:
        Problem: An instance of the Problem dataclass populated with parsed data.
    """
    question = json_data.get("data", {}).get("question", {})

    # Extract basic fields
    title = question.get("title", "")
    question_frontend_id = question.get("questionFrontendId", "")
    category_title = question.get("categoryTitle", "")
    difficulty = question.get("difficulty", "")
    topic_tags = [tag.get("name", "") for tag in question.get("topicTags", [])]

    # Parsing stats
    stats_str = question.get("stats", "{}")

    try:
        stats = json.loads(stats_str)

    except json.JSONDecodeError:
        stats = {}

    likes = question.get("likes", 0)
    dislikes = question.get("dislikes", 0)
    is_paid_only = question.get("isPaidOnly", False)
    solution_info = question.get("solution")
    code_snippets = question.get("codeSnippets", [])

    # Parsing HTML content
    content_html = question.get("content", "")
    soup = BeautifulSoup(content_html, "html.parser")

    description_parts = []
    examples = []
    constraints = []

    # Flag to indicate if we've entered the examples section
    in_examples = False

    # Iterate through all top-level elements
    for elem in soup.find_all(recursive=False):
        if elem.name == "p":
            # Check if it's an example
            strong_example = elem.find("strong", class_="example")
            if strong_example:
                in_examples = True  # Set the flag
                example_title = strong_example.get_text(strip=True).rstrip(":")

                # Find the next <pre> tag
                pre = elem.find_next_sibling("pre")
                if pre:
                    # Initialize the example dict
                    example = {
                        "title": example_title,
                        "input": [],
                        "output": "",
                        "explanation": "",
                    }

                    # Find all <strong> tags within <pre>
                    strong_tags = pre.find_all("strong")

                    # Initialize variables
                    current_section = None

                    for strong in strong_tags:
                        section_title = strong.get_text(strip=True).rstrip(":").lower()
                        current_section = section_title

                        # Get the content after the <strong> tag until the next <strong> tag
                        content = ""
                        for sibling in strong.next_siblings:
                            if isinstance(sibling, Tag) and sibling.name == "strong":
                                # Reached the next section
                                break

                            elif isinstance(sibling, Tag):
                                content += sibling.get_text(separator=" ", strip=True)

                            elif isinstance(sibling, NavigableString):
                                content += sibling.strip()

                        if current_section == "input":
                            if content:
                                example["input"].append(content)

                        elif current_section == "output":
                            if content:
                                example["output"] += content

                        elif current_section == "explanation":
                            # For explanation, capture all remaining content
                            explanation_content = []

                            for sib in strong.next_siblings:
                                if isinstance(sib, Tag):
                                    explanation_content.append(str(sib))

                                elif isinstance(sib, NavigableString):
                                    explanation_content.append(sib.strip())

                            example["explanation"] = "".join(
                                explanation_content
                            ).strip()

                    examples.append(example)
                continue  # Move to the next top-level element

            # Check if it's constraints
            strong_constraints = elem.find("strong")
            if strong_constraints and "Constraints" in strong_constraints.get_text():
                ul = elem.find_next_sibling("ul")
                if ul:
                    for li in ul.find_all("li"):
                        constraints.append(li.decode_contents().strip())

                continue

        # Accumulate description only if not in examples
        if not in_examples:
            description_parts.append(str(elem))

    # Combine description parts
    description = "".join(description_parts).strip()

    # Create the Problem instance
    problem = Problem(
        title=title,
        question_frontend_id=question_frontend_id,
        description=description,
        examples=examples,
        constraints=constraints,
        category_title=category_title,
        difficulty=difficulty,
        topic_tags=topic_tags,
        stats=stats,
        likes=likes,
        dislikes=dislikes,
        is_paid_only=is_paid_only,
        solution_info=solution_info,
        code_snippets=code_snippets,
    )

    return problem
