import src.scraper as scraper
import pandas as pd


class TestRetrieveData:
    """Test the retrieve_data function"""

    def test_retrieve_data_league_options(self):
        """Test league options only retrieves indicated league"""
        res = scraper.retrieve_data_leagues(mode='simple', league_option='baa')
        for r in res:
            assert r['League'] == "BAA"

    def test_retrieve_data_all_leagues(self):
        """Test all leagues return every row in the table"""
        res = scraper.retrieve_data_leagues(mode='simple', league_option='all')
        df = pd.DataFrame(res)
        assert len(df) == len(df.query('League == ["NBA", "ABA", "BAA"]'))

    def test_full_mode(self):
        """Test that full mode retrieves player data too"""
        res = scraper.retrieve_data_leagues(mode='full', league_option='aba')
        df = pd.DataFrame(res)
        assert df.query('Season == "1975-76"')['MVP'].item() == 'J. Erving'
