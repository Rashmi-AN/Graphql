import requests
import json

query = """
query ($cursor: String) {
  repository(owner: "sunbird-ed", name: "community") {
    discussions(first: 100, after: $cursor) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        locked
      }
    }
  }
}
"""

url = 'https://api.github.com/graphql'
headers = {"Authorization": "bearer "}

cursor = None
count = 0

while True:
    variables = {'cursor': cursor}
    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
    if response.status_code == 200:
        json_data = json.loads(response.text)
        discussions = json_data["data"]["repository"]["discussions"]["nodes"]
        count += len([d for d in discussions if d["locked"] is True])
        has_next_page = json_data["data"]["repository"]["discussions"]["pageInfo"]["hasNextPage"]
        if has_next_page:
            cursor = json_data["data"]["repository"]["discussions"]["pageInfo"]["endCursor"]
        else:
            break
    else:
        print("Request failed with status code:", response.status_code)
        break

print(f"Total count of locked discussions: {count}")
