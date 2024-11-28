GRAPHQL_URL = "https://leetcode.com/graphql"

GRAPHQL_QUERIES = {
    'problems_stats': """
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

    'problems_data': """
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
              freqBar
              frontendQuestionId: questionFrontendId
              isFavor
              paidOnly: isPaidOnly
              status
              title
              titleSlug
              topicTags {
                name
                id
                slug
              }
            }
          }
        }
    """,

    'code_snippets': """
        query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                codeSnippets {
                    lang
                    langSlug
                    code
                }
            }
        }
        """
}
