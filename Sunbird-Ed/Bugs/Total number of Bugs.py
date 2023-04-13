import json
import requests

query = """
query($cursor: String) {
  repository(owner: "sunbird-ed", name: "community") {
    discussions(first: 100, after: $cursor) {
      pageInfo {
        endCursor
        hasNextPage
      }
      nodes {
        id
        category {
          slug
        }
      }
    }
  }
}
"""

url = 'https://api.github.com/graphql'
headers = {"Authorization": "bearer "}

has_next_page = True
end_cursor = None
num_bugs = 0
discussions_seen = set()

while has_next_page:
    variables = {"cursor": end_cursor}
    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        json_data = json.loads(response.text)
        discussions = json_data["data"]["repository"]["discussions"]
        end_cursor = discussions["pageInfo"]["endCursor"]
        has_next_page = discussions["pageInfo"]["hasNextPage"]
        bug_discussions = [d for d in discussions["nodes"] if d["category"]["slug"] == "bugs" and d["id"] not in discussions_seen]

        num_bugs += len(bug_discussions)
        discussions_seen.update(d["id"] for d in bug_discussions)
    else:
        print("Request failed with status code:", response.status_code)
        break

print("Total number of bugs:", num_bugs)
