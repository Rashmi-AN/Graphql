import requests
import configparser

config = configparser.ConfigParser(interpolation=None)
config.read("Please add the config file path")

name_of_community = config.get("COMMUNITY_NAME", "name")

query = """query {
  repository(owner: "%s", name: "community") {
    discussions(first: 100) {
      # type: DiscussionConnection
      totalCount # Int!
    }
  }
}""" % name_of_community

token_details = config.get("BEARER", "token")

url = 'https://api.github.com/graphql'
headers = {"Authorization": "bearer " + token_details}
r = requests.post(url, headers=headers, json={'query': query})
print(r.status_code)
print(r.text)
