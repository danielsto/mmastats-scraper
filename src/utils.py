import json
import re
import requests
import bs4

BASE_URL = 'https://www.basketball-reference.com'
REGEX_NUMS = r'\d+|\d+\.\d+'
REGEX_NAMES = r'.+?(?=\s\()'

with open("./data/teams.json") as json_file:
    TEAMS = json.load(json_file)


def get_end_year(season):
    """
    Returns the end year given a season in YYYY-YY format
    """
    second_part = season.split('-')[1]
    first_part = '20' if second_part == '00' else season.split('-')[0][:2]
    year = f'{first_part}{second_part}'
    return int(year)


def treat_input(leader, type="integer"):
    """
    Returns the score given an input that has mixed name (string) and score
    (integer/float) like L. James (987).
    """
    if re.findall(REGEX_NUMS, leader):
        if type == "integer":
            score = int(re.findall(REGEX_NUMS, leader)[0])
        else:
            score = float(re.findall(REGEX_NUMS, leader)[0])
    else:
        score = None
    return score


def get_player_data(player, row, season, mode):
    """
    Scrapes player profile to return their contry, team and age
    """
    player_rel_url = row.find("td", {"data-stat": player}).find("a")

    if not player_rel_url or mode == 'simple':
        return None, None, None
    else:
        player_url = BASE_URL + player_rel_url['href']

    req = requests.get(player_url)
    status_code = req.status_code

    if status_code == 200:
        soup = bs4.BeautifulSoup(req.text, "html.parser")

        if soup.find("span", {"class": "f-i f-us"}):
            country_text = "United States"
        else:
            country_a = soup.find("span", {"itemprop": "birthPlace"})
            country = country_a.find("a") if country_a else None
            country_text = country.text if country else None

        team_id = soup.find("tr", {"id": f'per_game.{get_end_year(season)}'}).find("td", {"data-stat": "team_id"}).text if soup.find("tr", {"id": f'per_game.{get_end_year(season)}'}) else None
        team = TEAMS[team_id] if team_id else None

        birth_date = soup.find("span", {"itemprop": "birthDate"})['data-birth'] if soup.find("span", {"itemprop": "birthDate"}) else None
        age_awarded = get_end_year(season) - int(birth_date.split('-')[0]) if birth_date else None
        return country_text, team, int(age_awarded) if age_awarded else None
    else:
        print(f'[Player] \033[31mERROR {status_code}\033[0m')
        return None, None, None
