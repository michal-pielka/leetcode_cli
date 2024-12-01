from .data_fetching.leetcode_stats import fetch_leetcode_stats, fetch_leetcode_activity
from .data_fetching.fetch_code_snippet import fetch_code_snippet
from .data_fetching.leetcode_problem_fetcher import LeetCodeProblemFetcher

from .parsers.parser_utils.leetcode_stats_parser import *
from .parsers.submission_parser import parse_submission
from .parsers.leetcode_stats_parser import parse_leetcode_stats, parse_daily_activity
from .parsers.leetcode_problem_parser import LeetCodeProblemParser
from .parsers.leetcode_problemset_parser import LeetCodeProblemsetParser

from .parsers.parser_utils.leetcode_stats_parser import *

# Test parsing stats
def parse_stats():
    username = "BucketAbuser"
    user_stats = fetch_leetcode_stats(username)

    parsed_stats = parse_leetcode_stats(user_stats)
    print(parsed_stats)

def parse_activity():
    username = "BucketAbuser"
    y1activ = fetch_leetcode_activity(username, 2024)
    y2activ = fetch_leetcode_activity(username, 2023)

    joinedActiv = join_and_slice_calendars(y2activ, y1activ)
    filledActiv = fill_daily_activity(joinedActiv)

    parsed = parse_daily_activity(filledActiv)
    print(parsed)


def parse_problem(title_slug = "house-robber"):
    problem = LeetCodeProblemFetcher()
    metadata = problem.fetch_problem_data(title_slug)

    parser = LeetCodeProblemParser(metadata)

    print(parser.get_formatted_title())
    print()
    print(parser.get_formatted_topic_tags())
    print()
    print(parser.get_formatted_languages())
    print(parser.get_formatted_description())
    print(parser.get_formatted_examples())
    print()
    print(parser.get_formatted_constraints())

def parse_problemset():
    tags = []
    difficulty = "Medium" 
    limit = 50
    skip = 0
    category_slug = "all-code-essentials"
    problems_dict = LeetCodeProblemFetcher.fetch_problemset(tags = tags, difficulty = difficulty, limit = limit, skip = skip, category_slug=category_slug)

    parser = LeetCodeProblemsetParser(problems_dict)
    s = parser.parse_questions()
    print(s)

#parse_stats()
#parse_activity()
parse_problemset()
