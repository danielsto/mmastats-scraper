from src.utils import get_player_data, get_end_year, treat_input
from src.utils import REGEX_NUMS, REGEX_NAMES
import bs4

SAMPLE_HTML = '<tr data-row="1"><th scope="row" class="left " data-stat="season"><a href="/leagues/NBA_2020.html">2019-20</a></th><td class="left " data-stat="lg_id"><a href="/leagues/NBA_2020.html">NBA</a></td><td class="left " data-stat="champion"><a href="/teams/LAL/2020.html">Los Angeles Lakers</a></td><td class="left " data-stat="mvp"><a href="/players/a/antetgi01.html">G. Antetokounmpo</a></td><td class="left " data-stat="roy"><a href="/players/m/moranja01.html">J. Morant</a></td><td class="left " data-stat="pts_leader_name"><a href="/players/h/hardeja01.html">J. Harden</a>&nbsp;(2335)</td><td class="left " data-stat="trb_leader_name"><a href="/players/g/goberru01.html">R. Gobert</a>&nbsp;(916)</td><td class="left " data-stat="ast_leader_name"><a href="/players/j/jamesle01.html">L. James</a>&nbsp;(684)</td><td class="left " data-stat="ws_leader_name"><a href="/players/h/hardeja01.html">J. Harden</a>&nbsp;(13.1)</td></tr>'
MOCK_ROW = bs4.BeautifulSoup(SAMPLE_HTML, "html.parser")


class TestTreatInput:
    """Test the treat_input function"""

    def test_normal_integer_input(self):
        """Test that the right integer is returned from a mixed string"""
        pts_leader = 'K. Bryant (2832)'
        res = treat_input(pts_leader)
        assert res, 2832

    def test_normal_decimal_input(self):
        """Test that the right decimal is returned from a mixed string"""
        ws_leader = "S. O'Neal (14.9)"
        res = treat_input(ws_leader)
        assert res, 14.9


class TestGetEndYear:
    """Test get_end_year function"""

    def test_21st_century(self):
        """Test for years in the 21st century"""
        season = '2019-20'
        res = get_end_year(season)
        assert res == 2020

    def test_20th_century(self):
        """Test for years in the 20th century"""
        season = '1989-90'
        res = get_end_year(season)
        assert res == 1990

    def test_year_2000(self):
        """Test in the change of century/millenium"""
        season = '1999-00'
        res = get_end_year(season)
        assert res == 2000


class TestGetPlayerData:
    """Test get_player_data function"""

    def test_simple_mode(self):
        res = get_player_data("roy", MOCK_ROW, '2019-20', "simple")
        assert res == (None, None, None)

    def test_full_mode(self):
        res = get_player_data("roy", MOCK_ROW, '2019-20', "full")
        assert res == ('United States', 'Memphis Grizzlies', 21)
