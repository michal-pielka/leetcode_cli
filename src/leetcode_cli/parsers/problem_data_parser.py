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
    content_html = question.get("content", "") or ""
    soup = BeautifulSoup(content_html, "html.parser")

    description_parts = []
    examples = []
    constraints = []

    # Whether we have begun parsing examples
    in_examples = False

    # Iterate through all top-level elements
    for elem in soup.find_all(recursive=False):
        # A <p> with <strong class="example"> indicates the start of an example
        if elem.name == "p":
            strong_example = elem.find("strong", class_="example")
            if strong_example:
                in_examples = True
                # e.g. "Example 1:", "Example 2:"
                example_title = strong_example.get_text(strip=True).rstrip(":")

                # We'll attempt two patterns:
                #   A) If next sibling is <div class="example-block"> => parse that
                #   B) Else walk siblings to find a <pre> (old style)

                # Let's find siblings until we see either <div class="example-block"> or <pre> or we run out
                sibling = elem.next_sibling
                pre_tag = None
                example_div = None

                while sibling:
                    if isinstance(sibling, Tag):
                        # Check if it's a <div class="example-block">
                        if sibling.name == "div" and "example-block" in sibling.get(
                            "class", []
                        ):
                            example_div = sibling
                            break
                        # Or if it's <pre> (old style approach)
                        if sibling.name == "pre":
                            pre_tag = sibling
                            break
                    sibling = sibling.next_sibling

                # Now parse accordingly
                if example_div:
                    # Newer approach: parse the <div class="example-block"> for p strong: "Input", "Output", "Explanation"
                    ex_obj = _parse_div_example_block(example_title, example_div)
                    examples.append(ex_obj)

                elif pre_tag:
                    # Old approach: parse <pre> for strong "Input"/"Output"/"Explanation"
                    ex_obj = _parse_pre_example_block(example_title, pre_tag)
                    examples.append(ex_obj)

                # Move on to next top-level element
                continue

            # Check if it’s constraints
            strong_constraints = elem.find("strong")
            if strong_constraints and "Constraints" in strong_constraints.get_text():
                ul = elem.find_next_sibling("ul")
                if ul:
                    for li in ul.find_all("li"):
                        constraints.append(li.decode_contents().strip())
                continue

        # If we haven't hit examples yet, it's description
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


def _parse_div_example_block(example_title: str, example_div: Tag) -> dict:
    """
    Handles the 'newer' style examples that look like:
      <div class="example-block">
         <p><strong>Input:</strong> ...</p>
         <p><strong>Output:</strong> ...</p>
         <p><strong>Explanation:</strong> ...</p>
         ...
      </div>

    Returns a dict { "title", "input", "output", "explanation" }
    """
    example = {
        "title": example_title,
        "input": [],
        "output": "",
        "explanation": "",
    }

    # We look for direct <p> tags with <strong> text like "Input:", "Output:", "Explanation:"
    # or variations. We'll store them accordingly.
    # If we want to be robust, we can also handle <ul> or subsequent lines for explanation.

    # For each <p> inside example_div:
    for p_tag in example_div.find_all("p", recursive=False):
        strong_tag = p_tag.find("strong")
        if not strong_tag:
            continue
        label_text = strong_tag.get_text(strip=True).rstrip(":").lower()
        # The content is the text outside the strong tag
        # e.g. in <p><strong>Input:</strong> <span>nums=...</span></p>
        # we want to gather the rest of the text or <span> after the strong
        # We'll do so by taking p_tag.get_text... but that might re-include "Input:" if not careful.

        # We'll build the content by ignoring the <strong> text:
        content = ""
        # after we skip the <strong> itself, gather siblings
        for sib in strong_tag.next_siblings:
            if isinstance(sib, NavigableString):
                content += sib.strip()
            elif isinstance(sib, Tag):
                content += sib.get_text(separator=" ", strip=True)

        content = content.strip()

        if label_text == "input":
            # We do example["input"].append(...) or combine
            if content:
                example["input"].append(content)
        elif label_text == "output":
            example["output"] = content
        elif label_text == "explanation":
            example["explanation"] = content

    # Some example-blocks might have extra stuff (like <ul> for explanation),
    # so optionally we can parse more. For now, let's keep it simple.

    return example


def _parse_pre_example_block(example_title: str, pre_tag: Tag) -> dict:
    """
    Handles the 'old' style example using <pre> with multiple <strong> sections
    for "Input", "Output", "Explanation".
    """
    example = {
        "title": example_title,
        "input": [],
        "output": "",
        "explanation": "",
    }

    # Find all <strong> tags
    strong_tags = pre_tag.find_all("strong")
    current_section = None

    from bs4 import NavigableString, Tag

    for strong in strong_tags:
        section_title = strong.get_text(strip=True).rstrip(":").lower()
        current_section = section_title

        # Gather text after this <strong> until next <strong>
        content = ""
        for sibling in strong.next_siblings:
            if isinstance(sibling, Tag) and sibling.name == "strong":
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
                if isinstance(sib, Tag) and sib.name == "strong":
                    break
                elif isinstance(sib, Tag):
                    explanation_content.append(str(sib))
                elif isinstance(sib, NavigableString):
                    explanation_content.append(sib.strip())
            example["explanation"] = "".join(explanation_content).strip()

    return example
