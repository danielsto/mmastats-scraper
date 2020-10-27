import bs4
import requests
import re
import json
import pandas as pd
import sys

BASE_URL = 'https://www.basketball-reference.com/leagues/'

def retrieve_data_leagues():
    url = BASE_URL
    req = requests.get(url)
    status_code = req.status_code
    data_output = []
    headers = [
        "Season", "League", "Champion", "MVP", "ROTY", "Points Leader", 
        "Points", "Rebounds Leader", "Rebounds", "Assists Leader", "Assists", 
        "Win Share Leader", "Win Shares"
    ]

    if status_code == 200:
        print('\033[92m' + "200 OK" + '\033[0m')
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        rows = soup.find("table").find_all("tr")
        for i, r in enumerate(rows):
            if i < 2:
                continue

            season = r.find("th", {"data-stat": "season"}).text
            league = r.find("td", {"data-stat": "lg_id"}).text
            champion = r.find("td", {"data-stat": "champion"}).text
            mvp = r.find("td", {"data-stat": "mvp"}).text
            roy = r.find("td", {"data-stat": "roy"}).text
            pts_leader = r.find("td", {"data-stat": "pts_leader_name"}).text
            pts_leader_name = " ".join(re.findall(r'.+?(?=\s\()', pts_leader))
            pts_leader_score = int(re.findall(r'\d+|\d+\.\d+', pts_leader)[0]) if re.findall(r'\d+|\d+\.\d+', pts_leader) else None

            trb_leader = r.find("td", {"data-stat": "trb_leader_name"}).text
            trb_leader_name = " ".join(re.findall(r'.+?(?=\s\()', trb_leader))
            trb_leader_score = int(re.findall(r'\d+|\d+\.\d+', trb_leader)[0]) if re.findall(r'\d+|\d+\.\d+', trb_leader) else None
            
            ast_leader = r.find("td", {"data-stat": "ast_leader_name"}).text
            ast_leader_name = " ".join(re.findall(r'.+?(?=\s\()', ast_leader))
            ast_leader_score = int(re.findall(r'\d+|\d+\.\d+', ast_leader)[0]) if re.findall(r'\d+|\d+\.\d+', ast_leader) else None

            ws_leader = r.find("td", {"data-stat": "ws_leader_name"}).text
            ws_leader_name = " ".join(re.findall(r'.+?(?=\s\()', ws_leader))
            ws_leader_score = float(re.findall(r'\d+|\d+\.\d+', ws_leader)[0]) if re.findall(r'\d+|\d+\.\d+', ws_leader) else None

            res = {
                "Season": season,
                "League": league,
                "Champion": champion,
                "MVP": mvp,
                "ROTY": roy,
                "Points Leader": pts_leader_name,
                "Points": pts_leader_score,
                "Rebounds Leader": trb_leader_name,
                "Rebounds": trb_leader_score,
                "Assists Leader": ast_leader_name,
                "Assists": ast_leader_score,
                "Win Shares Leader": ws_leader_name,
                "Win Shares": ws_leader_score,
            }

            data_output.append(res)
        
        df = pd.DataFrame(data_output)
        print(df.describe())
        
        df.to_csv("nba.csv", index=False)
    else:
        print('\033[31m' + 'ERROR: selected URL could not be found'+ '\033[0m')
        exit()

if __name__ == "__main__":
    retrieve_data_leagues()

    