import json

BASE_URL = 'https://www.basketball-reference.com'
REGEX_NUMS = r'\d+|\d+\.\d+'
REGEX_NAMES = r'.+?(?=\s\()'

with open("./data/teams.json") as json_file:
    TEAMS = json.load(json_file)
