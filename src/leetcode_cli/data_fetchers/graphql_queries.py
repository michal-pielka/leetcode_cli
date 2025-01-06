GRAPHQL_URL = "https://leetcode.com/graphql"

GRAPHQL_QUERIES = {
    "user_problem_stats": """
        query userProfileUserQuestionProgressV2($userSlug: String!) {
          userProfileUserQuestionProgressV2(userSlug: $userSlug) {
            numAcceptedQuestions {
              count
              difficulty
            }
            numFailedQuestions {
              count
              difficulty
            }
            numUntouchedQuestions {
              count
              difficulty
            }
            userSessionBeatsPercentage {
              difficulty
              percentage
            }
            totalQuestionBeatsPercentage
          }
        }
    """,

    "user_calendar": """
        query userProfileCalendar($username: String!, $year: Int) {
          matchedUser(username: $username) {
            userCalendar(year: $year) {
              activeYears
              streak
              totalActiveDays
              dccBadges {
                timestamp
                badge {
                  name
                  icon
                }
              }
              submissionCalendar
            }
          }
        }
    """,

    "problemset_data": """
        query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
          problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
          ) {
            total: totalNum
            questions: data {
              acRate
              difficulty
              questionId
              topicTags {
                slug
              }
              frontendQuestionId: questionFrontendId
              paidOnly: isPaidOnly
              status
              title
              titleSlug
            }
          }
        }
    """,

    "problemset_metadata": """
        query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
          problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
          ) {
            total: totalNum
            questions: data {
              questionId
              frontendQuestionId: questionFrontendId
              titleSlug
            }
          }
        }
    """,

    "code_snippets": """
        query getQuestionDetail($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionId
            titleSlug
            codeSnippets {
              lang
              langSlug
              code
            }
          }
        }
    """,

    "problem_detail": """
        query questionDetail($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            title
            questionFrontendId
            questionTitle
            content
            categoryTitle
            difficulty
            topicTags {
              name
            }
            stats
            likes
            dislikes
            isPaidOnly
            solution {
              id
              paidOnly
              hasVideoSolution
              canSeeDetail
            }
            codeSnippets {
              lang
              langSlug
            }
          }
        }
    """,

    "random_title_slug": """
        query randomQuestion($categorySlug: String, $filters: QuestionListFilterInput) {
            randomQuestion(categorySlug: $categorySlug, filters: $filters) {
                titleSlug
            }
        }
    """,

    "problem_id": """
        query questionDetail($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionFrontendId
            questionId
          }
        }
    """,

    "problem_testcases": """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            exampleTestcases
          }
        }
    """
}
