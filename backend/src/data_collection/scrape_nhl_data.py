import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_nhl_data(season_urls):
    all_data = []

    for url in season_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        games = soup.find_all('tr', class_='')

        for game in games:
            date = game.find('th', {'data-stat': 'date_game'}).text if game.find('th', {'data-stat': 'date_game'}) else 'N/A'
            team1 = game.find('td', {'data-stat': 'visitor_team_name'}).text if game.find('td', {'data-stat': 'visitor_team_name'}) else 'N/A'
            team2 = game.find('td', {'data-stat': 'home_team_name'}).text if game.find('td', {'data-stat': 'home_team_name'}) else 'N/A'
            score1 = game.find('td', {'data-stat': 'visitor_goals'}).text if game.find('td', {'data-stat': 'visitor_goals'}) else 'N/A'
            score2 = game.find('td', {'data-stat': 'home_goals'}).text if game.find('td', {'data-stat': 'home_goals'}) else 'N/A'

            if 'N/A' not in [date, team1, team2, score1, score2]:
                all_data.append([date, team1, team2, score1, score2])
            else:
                print(f"Skipping game with missing data: {date}, {team1}, {team2}, {score1}, {score2}")

    df = pd.DataFrame(all_data, columns=['Date', 'Visitor Team', 'Home Team', 'Visitor Goals', 'Home Goals'])
    return df

if __name__ == "__main__":
    season_urls = [
        'https://www.hockey-reference.com/leagues/NHL_2023_games.html',
        'https://www.hockey-reference.com/leagues/NHL_2022_games.html',
        'https://www.hockey-reference.com/leagues/NHL_2021_games.html',
        'https://www.hockey-reference.com/leagues/NHL_2020_games.html',
        'https://www.hockey-reference.com/leagues/NHL_2019_games.html',
        'https://www.hockey-reference.com/leagues/NHL_2018_games.html',
        'https://www.hockey-reference.com/leagues/NHL_2017_games.html',
        'https://www.hockey-reference.com/leagues/NHL_2016_games.html',
        'https://www.hockey-reference.com/leagues/NHL_2015_games.html',
        'https://www.hockey-reference.com/leagues/NHL_2014_games.html',
        'https://www.hockey-reference.com/leagues/NHL_2013_games.html',
        'https://www.hockey-reference.com/leagues/NHL_2012_games.html',
    ]
    output_file = 'data/raw/nhl_game_data.csv'
    df = scrape_nhl_data(season_urls)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
