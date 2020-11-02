import bs4
import requests
import re
import pandas as pd
from utils import BASE_URL, REGEX_NAMES, REGEX_NUMS, TEAMS,\
                get_player_data, get_end_year, treat_input


def save_output_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("./data/nba.csv", index=False)


def retrieve_data_leagues(mode, league_option):
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
            print(r)
            season = r.find("th", {"data-stat": "season"}).text
            print(season)
            league = r.find("td", {"data-stat": "lg_id"}).text

            if league_option != (league.lower() or "all"):
                continue

            champion = r.find("td", {"data-stat": "champion"}).text
            mvp = r.find("td", {"data-stat": "mvp"}).text
            mvp_country, mvp_team, mvp_age = get_player_data("mvp", r, season, mode)

            roy = r.find("td", {"data-stat": "roy"}).text
            roy_country, roy_team, roy_age = get_player_data("roy", r, season, mode)

            pts_leader = r.find("td", {"data-stat": "pts_leader_name"}).text
            pts_leader_name = " ".join(re.findall(REGEX_NAMES, pts_leader))
            pts_leader_score = treat_input(pts_leader)
            pts_country, pts_team, pts_age = \
                get_player_data("pts_leader_name", r, season, mode)

            trb_leader = r.find("td", {"data-stat": "trb_leader_name"}).text
            trb_leader_name = " ".join(re.findall(REGEX_NAMES, trb_leader))
            trb_leader_score = treat_input(trb_leader)
            trb_country, trb_team, trb_age = \
                get_player_data("trb_leader_name", r, season, mode)

            ast_leader = r.find("td", {"data-stat": "ast_leader_name"}).text
            ast_leader_name = " ".join(re.findall(REGEX_NAMES, ast_leader))
            ast_leader_score = treat_input(ast_leader)
            ast_country, ast_team, ast_age = \
                get_player_data("ast_leader_name", r, season, mode)

            ws_leader = r.find("td", {"data-stat": "ws_leader_name"}).text
            ws_leader_name = " ".join(re.findall(REGEX_NAMES, ws_leader))
            print(ws_leader)
            ws_leader_score = treat_input(ws_leader, "decimal")
            ws_country, ws_team, ws_age = \
                get_player_data("ws_leader_name", r, season, mode)

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
