import json
import re
from bs4 import BeautifulSoup
from leetcode_cli.exceptions.exceptions import ParsingError
from leetcode_cli.models.problem import Problem

def parse_problem_data(json_data):
    if "data" not in json_data or "question" not in json_data["data"]:
        raise ParsingError("Invalid problem data structure: 'data.question' key not found.")

    question = json_data["data"]["question"]
    required_fields = ["title", "questionFrontendId", "content", "categoryTitle", "difficulty", 
                       "topicTags", "stats", "likes", "dislikes", "isPaidOnly", "solution", "codeSnippets"]

    for field in required_fields:
        if field not in question:
            raise ParsingError(f"Missing '{field}' in problem data.")

    # Parse topic tags
    topic_tags = []
    for tag_data in question["topicTags"]:
        if "name" not in tag_data:
            raise ParsingError("Topic tag data is missing 'name' field.")
        topic_tags.append(tag_data["name"])

    # Parse stats
    stats_str = question["stats"]
    stats_data = json.loads(stats_str)
    stats_required = ["totalAccepted", "totalSubmission", "totalAcceptedRaw", "totalSubmissionRaw", "acRate"]
    for sfield in stats_required:
        if sfield not in stats_data:
            raise ParsingError(f"Missing '{sfield}' in stats data.")

    stats = {
        "total_accepted": stats_data["totalAccepted"],
        "total_submission": stats_data["totalSubmission"],
        "total_accepted_raw": stats_data["totalAcceptedRaw"],
        "total_submission_raw": stats_data["totalSubmissionRaw"],
        "ac_rate": stats_data["acRate"]
    }

    # Parse solution info
    solution_data = question["solution"]
    if solution_data:
        solution_required = ["id", "paidOnly", "hasVideoSolution", "canSeeDetail"]
        for sol_field in solution_required:
            if sol_field not in solution_data:
                raise ParsingError(f"Missing '{sol_field}' in solution data.")

        solution_info = {
            "id": solution_data["id"],
            "paid_only": solution_data["paidOnly"],
            "has_video_solution": solution_data["hasVideoSolution"],
            "can_see_detail": solution_data["canSeeDetail"]
        }

    else:
        solution_info = None

    # Parse code snippets
    snippets = []
    print(question)
    for snippet_data in question["codeSnippets"]:
        snippet_required = ["lang", "langSlug"]
        for sn_field in snippet_required:
            if sn_field not in snippet_data:
                raise ParsingError(f"Missing '{sn_field}' in code snippet data.")

        snippets.append({
            "lang": snippet_data["lang"],
            "lang_slug": snippet_data["langSlug"]
        })

    # Parse the HTML content for description, examples, and constraints
    html_content = question["content"]
    soup = BeautifulSoup(html_content, "html.parser")

    # Find constraints
    constraints_header = soup.find('strong', string=re.compile(r'Constraints:'))
    constraints = []
    if constraints_header:
        ul_tag = constraints_header.find_next('ul')
        if ul_tag:
            # Keep HTML tags in constraints
            for li in ul_tag.find_all('li'):
                constraints.append(str(li))

    # Find examples by <strong class="example">
    example_headers = soup.find_all('strong', class_='example')
    examples = []
    for header in example_headers:
        example = _parse_example_section(header)
        if example:
            examples.append(example)

    # Determine earliest stop point
    stopping_points = []
    if example_headers:
        stopping_points.extend(example_headers)

    earliest_stop = None
    if stopping_points:
        all_elements = list(soup.find_all())
        earliest_stop = min(stopping_points, key=lambda el: all_elements.index(el))

    # Text-based slicing of the original HTML up to earliest_stop
    description_html = "Description not available"
    if earliest_stop:
        earliest_html = str(earliest_stop)
        idx = html_content.find(earliest_html)
        if idx != -1:
            # Slice everything up to earliest_stop's occurrence
            description_html = html_content[:idx]
        else:
            # If not found, fallback
            description_html = html_content
    else:
        # If no stop found, entire content is description
        description_html = html_content

    # Now clean up trailing empty paragraphs
    # We'll re-parse, remove trailing empty <p>, and then convert back to string.
    desc_soup = BeautifulSoup(description_html, "html.parser")
    _remove_trailing_empty_paragraphs(desc_soup)
    description_html = str(desc_soup).strip()


    problem = Problem(
        title=question["title"],
        question_frontend_id=question["questionFrontendId"],
        description=description_html,
        examples=examples,
        constraints=constraints,
        category_title=question["categoryTitle"],
        difficulty=question["difficulty"],
        topic_tags=topic_tags,
        stats=stats,
        likes=question["likes"],
        dislikes=question["dislikes"],
        is_paid_only=question["isPaidOnly"],
        solution_info=solution_info,
        code_snippets=snippets
    )

    return problem

def _parse_example_section(header):
    example_title = header.get_text(strip=True).rstrip(':')
    pre_tag = header.find_next('pre')
    if not pre_tag:
        return None
    example_content = pre_tag.decode_contents()
    return _parse_example_content(example_content, example_title)

def _parse_example_content(html_content: str, title: str) -> dict:
    soup = BeautifulSoup(html_content, "html.parser")
    content_text = soup.get_text(separator="\n").strip()
    example_dict = {"title": title}

    input_match = re.search(r'Input:\s*(.*?)(?:\nOutput:|\Z)', content_text, re.DOTALL)
    output_match = re.search(r'Output:\s*(.*?)(?:\nExplanation:|\Z)', content_text, re.DOTALL)
    explanation_match = re.search(r'Explanation:\s*(.*)', content_text, re.DOTALL)

    input_str = input_match.group(1).strip() if input_match else ""
    input_list = []
    if input_str:
        parts = [part.strip() for part in input_str.split(',')]
        input_list = [p for p in parts if p]

    example_dict['input'] = input_list
    example_dict['output'] = output_match.group(1).strip() if output_match else ""
    example_dict['explanation'] = explanation_match.group(1).strip() if explanation_match else ""

    return example_dict

def _remove_trailing_empty_paragraphs(soup: BeautifulSoup):
    """
    Removes trailing empty <p> tags (or those containing only &nbsp;) at the end of the document.
    """
    # Get all top-level elements
    elements = soup.find_all(recursive=False)
    for element in reversed(elements):
        if element.name == "p":
            txt = element.get_text(strip=True)
            if not txt or txt == '\xa0':
                element.decompose()
            else:
                # As soon as we find a non-empty paragraph, we stop removing
                break
        else:
            # Non-p element encountered, stop removing
            break
