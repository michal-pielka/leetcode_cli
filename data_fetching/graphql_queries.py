GRAPHQL_URL = "https://leetcode.com/graphql"

GRAPHQL_QUERIES = {
    'problem_stats': """
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

    'user_calendar': """
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

    'problemset_data': """
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

    'code_snippets': """
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

    'problem_data': """
        query questionData($titleSlug: String!) {
          submittableLanguageList {
            id
            name
            verboseName
          }
          question(titleSlug: $titleSlug) {
            questionId
            frontendQuestionId: questionFrontendId
            title
            titleSlug
            content
            difficulty
            likes
            dislikes
            exampleTestcases
            topicTags {
              name
              slug
            }
            hints
            isPaidOnly
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
