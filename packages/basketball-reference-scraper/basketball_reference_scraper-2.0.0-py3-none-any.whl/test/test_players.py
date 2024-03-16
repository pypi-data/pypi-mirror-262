import unittest
from basketball_reference_scraper.players import get_stats, get_game_logs, get_player_headshot

class TestPlayers(unittest.TestCase):
    def test_get_stats(self):
        expected_columns_season = ['SEASON', 'AGE', 'TEAM', 'LEAGUE', 'POS', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'AWARDS']
        expected_columns_playoffs = ['SEASON', 'AGE', 'TEAM', 'LEAGUE', 'POS', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        df = get_stats('Joe Johnson')
        self.assertCountEqual(list(df.columns), expected_columns_season)

        df = get_stats('LaMarcus Aldridge') 
        self.assertCountEqual(list(df.columns), expected_columns_season)

        df = get_stats('LaMarcus Aldridge', career=True)
        self.assertCountEqual(list(df.columns), expected_columns_season)

        df = get_stats('LaMarcus Aldridge', playoffs=True, career=True)
        self.assertCountEqual(list(df.columns), expected_columns_playoffs)

    def test_get_game_logs(self):
        expected_columns = ['DATE', 'AGE', 'TEAM', 'HOME/AWAY', 'OPPONENT', 'RESULT', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GAME_SCORE', '+/-']

        df = get_game_logs('Stephen Curry', 2022) 
        self.assertCountEqual(list(df.columns), expected_columns)

        df = get_game_logs('Pau Gasol', 2010, playoffs=False)
        self.assertEqual(len(df), 82)

    def test_get_player_headshot(self):
        expected_url = 'https://d2cwpp38twqe55.cloudfront.net/req/202006192/images/players/bryanko01.jpg'
        url = get_player_headshot('Kobe Bryant')
        self.assertEqual(url, expected_url)


if __name__ == '__main__':
    unittest.main()
