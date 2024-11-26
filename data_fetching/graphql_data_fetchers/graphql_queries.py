GRAPHQL_URL = "https://leetcode.com/graphql"

GRAPHQL_QUERIES = {

    'user_stats' : """
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

    'fetch_problems' : """
    query problemList($skip: Int!, $limit: Int!) {
      problemsetQuestionList(
        categorySlug: ""
        limit: $limit
        skip: $skip
        filters: {}
      ) {
        total
        questions {
          title
          titleSlug
          questionId
          isPaidOnly
          difficulty
          topicTags {
            name
            slug
          }
        }
      }
    }
    """

}
