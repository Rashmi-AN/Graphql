import requests
query = """query {
  repository(owner: "sunbird-ed", name: "community") {
    discussions(first: 100) {
      # type: DiscussionConnection
      totalCount # Int!
    }
  }
}"""


# res = requests.post('https://api.github.com/graphql',header)
url = 'https://api.github.com/graphql'
headers = {"Authorization": "bearer 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"}
r = requests.post(url, headers=headers, json={'query': query})
print(r.status_code)
print(r.text)
