import bs4
import requests
import re
import pandas as pd

BASE_URL = 'https://www.basketball-reference.com'
REGEX_NUMS = r'\d+|\d+\.\d+'
REGEX_NAMES = r'.+?(?=\s\()'


def save_output_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("nba.csv", index=False)


def get_end_year(season):
    first_part = season.split('-')[0][:2]
    second_part = season.split('-')[1]
    year = f'{first_part}{second_part}'
    return int(year)


def treat_input(leader, type="integer"):
    if re.findall(REGEX_NUMS, leader):
        if type == "integer":
            score = int(re.findall(REGEX_NUMS, leader)[0])
        else:
            score = float(re.findall(REGEX_NUMS, leader)[0])
    else:
        score = None
    return score


def get_player_data(player, row, season):
    player_rel_url = row.find("td", {"data-stat": player}).find("a")
    if not player_rel_url:
        return None, None, None
    else:
        player_url = BASE_URL + player_rel_url['href']
    req = requests.get(player_url)
    status_code = req.status_code
    if status_code == 200:
        # print('[Player] \033[92m200 OK\033[0m')
        soup = bs4.BeautifulSoup(req.text, "html.parser")

        if soup.find("span", {"class": "f-i f-us"}):
            country = "United States"
        else:
            country_link = soup.find("span", {"itemprop": "birthPlace"}).find("a")
            country = country_link.text if country_link else None

        team = soup.find("a", string=season).find_next("td", {"data-stat": "team_id"}).text
        birth_date = soup.find("span", {"itemprop": "birthDate"})['data-birth']
        age_awarded = get_end_year(season) - int(birth_date.split('-')[0])
        return country, team, age_awarded
    else:
        print(f'[Player] \033[31mERROR {status_code}\033[0m')
        return None, None, None


def retrieve_data_leagues():
    url = BASE_URL + '/leagues'
    req = requests.get(url)
    status_code = req.status_code
    data_output = []

    if status_code == 200:
        print('[Leagues] \033[92m200 OK\033[0m')
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        rows = soup.find("table").find_all("tr")
        for i, r in enumerate(rows):
            if i < 2:
                continue

            season = r.find("th", {"data-stat": "season"}).text
            print(season)
            league = r.find("td", {"data-stat": "lg_id"}).text
            champion = r.find("td", {"data-stat": "champion"}).text
            mvp = r.find("td", {"data-stat": "mvp"}).text
            mvp_country, mvp_team, mvp_age = get_player_data("mvp", r, season)

            roy = r.find("td", {"data-stat": "roy"}).text
            roy_country, roy_team, roy_age = get_player_data("roy", r, season)

            pts_leader = r.find("td", {"data-stat": "pts_leader_name"}).text
            pts_leader_name = " ".join(re.findall(REGEX_NAMES, pts_leader))
            pts_leader_score = treat_input(pts_leader)
            pts_country, pts_team, pts_age = \
                get_player_data("pts_leader_name", r, season)

            trb_leader = r.find("td", {"data-stat": "trb_leader_name"}).text
            trb_leader_name = " ".join(re.findall(REGEX_NAMES, trb_leader))
            trb_leader_score = treat_input(trb_leader)
            trb_country, trb_team, trb_age = \
                get_player_data("trb_leader_name", r, season)

            ast_leader = r.find("td", {"data-stat": "ast_leader_name"}).text
            ast_leader_name = " ".join(re.findall(REGEX_NAMES, ast_leader))
            ast_leader_score = treat_input(ast_leader)
            ast_country, ast_team, ast_age = \
                get_player_data("ast_leader_name", r, season)

            ws_leader = r.find("td", {"data-stat": "ws_leader_name"}).text
            ws_leader_name = " ".join(re.findall(REGEX_NAMES, ws_leader))
            ws_leader_score = treat_input(ws_leader, "decimal")
            ws_country, ws_team, ws_age = \
                get_player_data("ws_leader_name", r, season)

            res = {
                "Season": season,
                "League": league,
                "Champion": champion,
                "MVP": mvp,
                "MVP Age": mvp_age,
                "MVP Team": mvp_team,
                "MVP Country": mvp_country,
                "ROTY": roy,
                "ROTY Age": roy_age,
                "ROTY Team": roy_team,
                "ROTY Country": roy_country,
                "Points Leader": pts_leader_name,
                "Points": pts_leader_score,
                "Pts Age": pts_age,
                "Pts Team": pts_team,
                "Pts Country": pts_country,
                "Rebounds Leader": trb_leader_name,
                "Rebounds": trb_leader_score,
                "Rb Age": trb_age,
                "Rb Team": trb_team,
                "Rb Country": trb_country,
                "Assists Leader": ast_leader_name,
                "Assists": ast_leader_score,
                "Ast Age": ast_age,
                "Ast Team": ast_team,
                "Ast Country": ast_country,
                "Win Shares Leader": ws_leader_name,
                "Win Shares": ws_leader_score,
                "WS Age": ws_age,
                "WS Team": ws_team,
                "WS Country": ws_country,
            }
            data_output.append(res)
        return data_output
    else:
        print(f'[Leagues] \033[31mERROR {status_code}\033[0m')


if __name__ == "__main__":
    data = retrieve_data_leagues()
    save_output_csv(data)
