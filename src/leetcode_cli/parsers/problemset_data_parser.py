from typing import Dict, Any
from leetcode_cli.exceptions.exceptions import ParsingError
from leetcode_cli.models.problemset import ProblemSet, ProblemSummary

def parse_problemset_data(json_data: Dict[str, Any]) -> ProblemSet:
    """
    Parses the JSON returned by fetch_problemset into a ProblemSet model.
    """
    if "data" not in json_data or "problemsetQuestionList" not in json_data["data"]:
        raise ParsingError("Invalid problemset data structure: 'data.problemsetQuestionList' key not found.")

    plist = json_data["data"]["problemsetQuestionList"]

    if "questions" not in plist or "total" not in plist:
        raise ParsingError("Missing 'questions' or 'total' in problemset data.")

    total = plist["total"]
    questions_data = plist["questions"]

    questions = []
    for q in questions_data:
        # Validate required fields
        required_fields = ["acRate", "difficulty", "questionId", "topicTags", "frontendQuestionId", "paidOnly", "status", "title", "titleSlug"]
        for field in required_fields:
            if field not in q:
                raise ParsingError(f"Missing '{field}' in question data.")

        # Extract topic tags (list of slugs)
        topic_slugs = [tag["slug"] for tag in q.get("topicTags", []) if "slug" in tag]

        summary = ProblemSummary(
            ac_rate=float(q["acRate"]),
            difficulty=q["difficulty"],
            question_id=str(q["questionId"]),
            topic_tags=topic_slugs,
            frontend_question_id=str(q["frontendQuestionId"]),
            paid_only=bool(q["paidOnly"]),
            status=q["status"],
            title=q["title"],
            title_slug=q["titleSlug"]
        )
        questions.append(summary)

    return ProblemSet(total=total, questions=questions)
