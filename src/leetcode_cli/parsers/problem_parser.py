test = {'data': {'question': {'title': 'Two Sum', 'questionFrontendId': '1', 'questionTitle': 'Two Sum', 'content': '<p>Given an array of integers <code>nums</code>&nbsp;and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p>\n\n<p>You may assume that each input would have <strong><em>exactly</em> one solution</strong>, and you may not use the <em>same</em> element twice.</p>\n\n<p>You can return the answer in any order.</p>\n\n<p>&nbsp;</p>\n<p><strong class="example">Example 1:</strong></p>\n\n<pre>\n<strong>Input:</strong> nums = [2,7,11,15], target = 9\n<strong>Output:</strong> [0,1]\n<strong>Explanation:</strong> Because nums[0] + nums[1] == 9, we return [0, 1].\n</pre>\n\n<p><strong class="example">Example 2:</strong></p>\n\n<pre>\n<strong>Input:</strong> nums = [3,2,4], target = 6\n<strong>Output:</strong> [1,2]\n</pre>\n\n<p><strong class="example">Example 3:</strong></p>\n\n<pre>\n<strong>Input:</strong> nums = [3,3], target = 6\n<strong>Output:</strong> [0,1]\n</pre>\n\n<p>&nbsp;</p>\n<p><strong>Constraints:</strong></p>\n\n<ul>\n\t<li><code>2 &lt;= nums.length &lt;= 10<sup>4</sup></code></li>\n\t<li><code>-10<sup>9</sup> &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>\n\t<li><code>-10<sup>9</sup> &lt;= target &lt;= 10<sup>9</sup></code></li>\n\t<li><strong>Only one valid answer exists.</strong></li>\n</ul>\n\n<p>&nbsp;</p>\n<strong>Follow-up:&nbsp;</strong>Can you come up with an algorithm that is less than <code>O(n<sup>2</sup>)</code><font face="monospace">&nbsp;</font>time complexity?', 'categoryTitle': 'Algorithms', 'difficulty': 'Easy', 'topicTags': [{'name': 'Array'}, {'name': 'Hash Table'}], 'stats': '{"totalAccepted": "15.4M", "totalSubmission": "28.3M", "totalAcceptedRaw": 15384162, "totalSubmissionRaw": 28308526, "acRate": "54.3%"}', 'likes': 59105, 'dislikes': 2112, 'isPaidOnly': False, 'solution': {'id': '7', 'paidOnly': False, 'hasVideoSolution': True, 'canSeeDetail': True}, 'codeSnippets': [{'code': 'class Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        \n    }\n};', 'lang': 'C++', 'langSlug': 'cpp'}, {'code': 'class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        \n    }\n}', 'lang': 'Java', 'langSlug': 'java'}, {'code': 'class Solution(object):\n    def twoSum(self, nums, target):\n        """\n        :type nums: List[int]\n        :type target: int\n        :rtype: List[int]\n        """\n        ', 'lang': 'Python', 'langSlug': 'python'}, {'code': 'class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        ', 'lang': 'Python3', 'langSlug': 'python3'}, {'code': '/**\n * Note: The returned array must be malloced, assume caller calls free().\n */\nint* twoSum(int* nums, int numsSize, int target, int* returnSize) {\n    \n}', 'lang': 'C', 'langSlug': 'c'}, {'code': 'public class Solution {\n    public int[] TwoSum(int[] nums, int target) {\n        \n    }\n}', 'lang': 'C#', 'langSlug': 'csharp'}, {'code': '/**\n * @param {number[]} nums\n * @param {number} target\n * @return {number[]}\n */\nvar twoSum = function(nums, target) {\n    \n};', 'lang': 'JavaScript', 'langSlug': 'javascript'}, {'code': 'function twoSum(nums: number[], target: number): number[] {\n    \n};', 'lang': 'TypeScript', 'langSlug': 'typescript'}, {'code': 'class Solution {\n\n    /**\n     * @param Integer[] $nums\n     * @param Integer $target\n     * @return Integer[]\n     */\n    function twoSum($nums, $target) {\n        \n    }\n}', 'lang': 'PHP', 'langSlug': 'php'}, {'code': 'class Solution {\n    func twoSum(_ nums: [Int], _ target: Int) -> [Int] {\n        \n    }\n}', 'lang': 'Swift', 'langSlug': 'swift'}, {'code': 'class Solution {\n    fun twoSum(nums: IntArray, target: Int): IntArray {\n        \n    }\n}', 'lang': 'Kotlin', 'langSlug': 'kotlin'}, {'code': 'class Solution {\n  List<int> twoSum(List<int> nums, int target) {\n    \n  }\n}', 'lang': 'Dart', 'langSlug': 'dart'}, {'code': 'func twoSum(nums []int, target int) []int {\n    \n}', 'lang': 'Go', 'langSlug': 'golang'}, {'code': '# @param {Integer[]} nums\n# @param {Integer} target\n# @return {Integer[]}\ndef two_sum(nums, target)\n    \nend', 'lang': 'Ruby', 'langSlug': 'ruby'}, {'code': 'object Solution {\n    def twoSum(nums: Array[Int], target: Int): Array[Int] = {\n        \n    }\n}', 'lang': 'Scala', 'langSlug': 'scala'}, {'code': 'impl Solution {\n    pub fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {\n        \n    }\n}', 'lang': 'Rust', 'langSlug': 'rust'}, {'code': '(define/contract (two-sum nums target)\n  (-> (listof exact-integer?) exact-integer? (listof exact-integer?))\n  )', 'lang': 'Racket', 'langSlug': 'racket'}, {'code': '-spec two_sum(Nums :: [integer()], Target :: integer()) -> [integer()].\ntwo_sum(Nums, Target) ->\n  .', 'lang': 'Erlang', 'langSlug': 'erlang'}, {'code': 'defmodule Solution do\n  @spec two_sum(nums :: [integer], target :: integer) :: [integer]\n  def two_sum(nums, target) do\n    \n  end\nend', 'lang': 'Elixir', 'langSlug': 'elixir'}]}}}
import json
import re
from bs4 import BeautifulSoup
from leetcode_cli.exceptions.exceptions import ParsingError
from leetcode_cli.models.problem import Problem

def parse_problem_data(json_data):
    """
    Parses the JSON returned by fetch_problem_data(title_slug) into a Problem model.
    Changes:
    - Trim description strictly before the first example or constraints section.
    - Constraints remain in HTML format (no stripping tags).
    - Strip only leading and trailing newlines from description.
    """

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

    # Parse stats (which might be a JSON string)
    stats_str = question["stats"]
    if isinstance(stats_str, str):
        try:
            stats_data = json.loads(stats_str)
        except json.JSONDecodeError:
            raise ParsingError("Stats field is not valid JSON.")
    else:
        stats_data = stats_str

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

    # Parse code snippets
    snippets = []
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
                # Store li as HTML
                constraints.append(str(li))

    # Find examples
    # Identify them by <strong class="example">
    example_headers = soup.find_all('strong', class_='example')
    examples = []
    for header in example_headers:
        example = _parse_example_section(header)
        if example:
            examples.append(example)

    # If no class='example', fallback to original pattern
    # Sometimes examples might not have class='example', but given instructions, let's trust that `class="example"` marks them.
    # If needed, we could also search by the regex 'Example \d+' as before:
    if not examples:
        # If no examples found by class, try fallback:
        fallback_example_headers = soup.find_all('strong', string=re.compile(r'Example \d+'))
        for header in fallback_example_headers:
            if header not in example_headers:
                example = _parse_example_section(header)
                if example:
                    examples.append(example)
                    example_headers.append(header)

    # Determine where description ends: the first element that is either an example or the constraints header.
    stopping_points = []
    if example_headers:
        stopping_points.extend(example_headers)
    if constraints_header:
        stopping_points.append(constraints_header)

    earliest_stop = None
    if stopping_points:
        # Sort stopping_points based on their occurrence in the HTML. The first found in the document order is earliest.
        all_elements = list(soup.find_all())
        earliest_stop = min(stopping_points, key=lambda el: all_elements.index(el))

    # If we found a stopping point, we slice the original HTML content up to that point
    if earliest_stop:
        description_html = _slice_html_before(html_content, earliest_stop, soup)
        # Strip only leading and trailing newlines
        description_html = description_html.strip('\n')
    else:
        description_html = html_content.strip('\n')

    problem = Problem(
        title=question["title"],
        question_frontend_id=question["questionFrontendId"],
        description=description_html.strip(),
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
    """
    Extract the example title and content.
    """
    example_title = header.get_text(strip=True).rstrip(':')
    pre_tag = header.find_next('pre')
    if not pre_tag:
        return None
    example_content = pre_tag.decode_contents()
    return _parse_example_content(example_content, example_title)

def _parse_example_content(html_content: str, title: str) -> dict:
    """
    Parses the content of an example into a dict: {title, input, output, explanation}.
    'input' will be a list of strings if multiple parameters are found.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    content_text = soup.get_text(separator="\n").strip()
    example_dict = {"title": title}

    input_match = re.search(r'Input:\s*(.*?)(?:\nOutput:|\Z)', content_text, re.DOTALL)
    output_match = re.search(r'Output:\s*(.*?)(?:\nExplanation:|\Z)', content_text, re.DOTALL)
    explanation_match = re.search(r'Explanation:\s*(.*)', content_text, re.DOTALL)

    input_str = input_match.group(1).strip() if input_match else ""
    input_list = []
    if input_str:
        # Split by ',' and strip each part
        parts = [part.strip() for part in input_str.split(',')]
        input_list = [p for p in parts if p]

    example_dict['input'] = input_list
    example_dict['output'] = output_match.group(1).strip() if output_match else ""
    example_dict['explanation'] = explanation_match.group(1).strip() if explanation_match else ""

    return example_dict

def _slice_html_before(original_html: str, stop_element, soup: BeautifulSoup) -> str:
    """
    Slices the original_html string to end right before the stop_element.
    We find the stop_element's exact HTML in the soup and use its start position
    in the original_html to slice.
    """
    # Convert stop_element to a string
    stop_html = str(stop_element)
    # Find where stop_html occurs in original_html
    idx = original_html.find(stop_html)
    if idx == -1:
        # If for some reason we can't find it, just return original_html (fallback)
        return original_html
    # Return everything up to idx (this excludes the stop_element and anything after it)
    sliced_html = original_html[:idx]

    # Now, strip leading and trailing newlines
    sliced_html = sliced_html.lstrip('\n').rstrip('\n')

    return sliced_html
