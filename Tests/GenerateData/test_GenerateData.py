import sys
import unittest
import statsapi

from Application.GenerateData.GenerateData import getWinLossRecords
from Application.GenerateData.GenerateData import getLineupIds
from Application.GenerateData.GenerateData import matchLineupWithPositions


class TestGenerateData(unittest.TestCase):

    def setUp(self):
        self.testDateStandingsFormat = '08/15/2020'
        self.testHomeIdWL = 133
        self.testAwayIdWL = 146

        self.validPositions = ['1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'P', 'C', 'DH']

        self.gameID1Lineups = 631508
        self.gameID1Boxscore = statsapi.boxscore_data(gamePk=self.gameID1Lineups)
        self.gameID1Home = [641313, 660162, 518735, 547989, 429665, 650391, 673357, 608577, 664901, 608337]
        self.gameID1HomePositions = ['SS', '3B', 'C', '1B', 'DH', 'LF', 'CF', 'RF', '2B', 'P']
        self.gameID1HomeLineupPositions = dict(zip(self.gameID1Home, self.gameID1HomePositions))
        self.gameID1Away = [543939, 669242, 502671, 641933, 572761, 666185, 451594, 668800, 664056, 425794]
        self.gameID1AwayPositions = ['2B', 'SS', '1B', 'DH', '3B', 'LF', 'RF', 'C', 'CF', 'P']
        self.gameID1AwayLineupPositions = dict(zip(self.gameID1Away, self.gameID1AwayPositions))

        self.gameID2Lineups = 566623
        self.gameID2Boxscore = statsapi.boxscore_data(gamePk=self.gameID2Lineups)
        self.gameID2Home = [451594, 669242, 502671, 542303, 657557, 593372, 543939, 446308, 657041, 425794]
        self.gameID2HomePositions = ['RF', '3B', '1B', 'LF', 'SS', 'P', '2B', 'C', 'CF', 'P']
        self.gameID2HomeLineupPositions = dict(zip(self.gameID2Home, self.gameID2HomePositions))
        self.gameID2HomeLineupPositions.pop(593372, None)
        self.gameID2Away = [624428, 668804, 516782, 605137, 591741, 592567, 621028, 466320, 553869, 605397]
        self.gameID2AwayPositions = ['2B', 'LF', 'CF', '1B', 'RF', '3B', 'SS', 'PH', 'C', 'P']
        self.gameID2AwayLineupPositions = dict(zip(self.gameID2Away, self.gameID2AwayPositions))
        self.gameID2AwayLineupPositions.pop(466320, None)


################################################################################
# getWinLossRecords - pass in the Home Team ID, Away Team ID, and the date of
# of the game in MM/DD/YYYY format and return a list of the home and away team
# wins and losses in format [homeWin, homeLoss, awayWin, awayLoss]
#
# Use Cases:
# 1. Get the Wins and Losses for both valid team id's at that date in the season
# 2. Unable to find one or both team IDs
#
################################################################################

    def test_getWinLossRecords_validIDs(self):
        self.assertIsInstance(getWinLossRecords(self.testHomeIdWL, self.testAwayIdWL, self.testDateStandingsFormat), list)
        self.assertEqual([15, 6, 9, 5], getWinLossRecords(self.testHomeIdWL, self.testAwayIdWL, self.testDateStandingsFormat))


    def test_getWinLossRecords_unableToFindId(self):
        self.assertIsInstance(getWinLossRecords(self.testHomeIdWL, 0, self.testDateStandingsFormat), list)
        self.assertIsInstance(getWinLossRecords(0, self.testAwayIdWL, self.testDateStandingsFormat), list)
        self.assertIsInstance(getWinLossRecords(0, 0, self.testDateStandingsFormat), list)
        self.assertEqual([15, 6, None, None], getWinLossRecords(self.testHomeIdWL, 0, self.testDateStandingsFormat))
        self.assertEqual([None, None, 9, 5], getWinLossRecords(0, self.testAwayIdWL, self.testDateStandingsFormat))
        self.assertEqual([None, None, None, None], getWinLossRecords(0, 0, self.testDateStandingsFormat))

################################################################################
# getLineupIds - pass in the retrieved boxscore and return the player IDs in list
# format for the home and away teams. Each list should contain 10 player IDs for
# the 9 players batting, and the starting pitcher's ID.
#
# Use Cases:
# 1. Get the player IDs for both teams with the given game ID
#
################################################################################

    def test_getLineupIds_validGame(self):
        checkHomeLineup, checkAwayLineup = getLineupIds(self.gameID1Boxscore)
        self.assertEqual(self.gameID1Home, checkHomeLineup)
        self.assertEqual(self.gameID1Away, checkAwayLineup)
        checkHomeLineup, checkAwayLineup = getLineupIds(self.gameID2Boxscore)
        self.assertEqual(self.gameID2Home, checkHomeLineup)
        self.assertEqual(self.gameID2Away, checkAwayLineup)

################################################################################
# matchLineupWithPositions - pass team id list, home or away team type and
# boxscore data to assign positions to the ordered team ID list
#
# Use Cases:
# 1. Valid player IDs result in dictionary with starting positions
# 2. Dictionary contains 10 players with a starting DH, 9 with only a pitcher.
# 3. Invalid player ID in team list results in empty dictionary
# 4. Invalid boxscore results in empty dictionary
# 5. Invalid team type passed in == {}. Valid types: ['home', 'away']
# 6. All starting positions must be represented in the dictionary list, if not,
#    return an empty dictionary
#
################################################################################

    def test_matchLineupWithPositions_validIdList(self):
        self.assertEqual(self.gameID1HomeLineupPositions, matchLineupWithPositions(self.gameID1Home, 'home', self.gameID1Boxscore))
        self.assertEqual(self.gameID1AwayLineupPositions, matchLineupWithPositions(self.gameID1Away, 'away', self.gameID1Boxscore))
        self.assertEqual(self.gameID2HomeLineupPositions, matchLineupWithPositions(self.gameID2Home, 'home', self.gameID2Boxscore))
        self.assertEqual(self.gameID2AwayLineupPositions, matchLineupWithPositions(self.gameID2Away, 'away', self.gameID2Boxscore))


    def test_matchLineupWithPositions_validLineupSizes(self):
        self.assertEqual(10, len(matchLineupWithPositions(self.gameID1Home, 'home', self.gameID1Boxscore)))
        self.assertEqual(10, len(matchLineupWithPositions(self.gameID1Away, 'away', self.gameID1Boxscore)))
        self.assertEqual(9, len(matchLineupWithPositions(self.gameID2Home, 'home', self.gameID2Boxscore)))
        self.assertEqual(9, len(matchLineupWithPositions(self.gameID2Away, 'away', self.gameID2Boxscore)))


    def test_matchLineupWithPositions_invalidPlayerIdList(self):
        self.assertEqual({}, matchLineupWithPositions(['stuff', 'things'], 'home', self.gameID1Boxscore))
        self.assertEqual({}, matchLineupWithPositions([], 'home', self.gameID1Boxscore))
        self.assertEqual({}, matchLineupWithPositions(self.gameID1Away, 'home', self.gameID1Boxscore))


    def test_matchLineupWithPositions_invalidBoxscore(self):
        self.assertEqual({}, matchLineupWithPositions(self.gameID1Home, 'home', {}))
        self.assertEqual({}, matchLineupWithPositions(self.gameID1Home, 'home', self.gameID2Boxscore))


    def test_matchLineupWithPositions_invalidTeamType(self):
        self.assertEqual({}, matchLineupWithPositions(self.gameID1Home, 'garbage', self.gameID1Boxscore))
        self.assertEqual({}, matchLineupWithPositions(['stuff'], 'things', {}))


    def test_matchLineupWithPositions_positionRepresentation(self):
        self.assertEqual(True, self.checkPositionValidity(matchLineupWithPositions(self.gameID1Home, 'home', self.gameID1Boxscore)))
        self.assertEqual(True, self.checkPositionValidity(matchLineupWithPositions(self.gameID1Away, 'away', self.gameID1Boxscore)))
        self.assertEqual(True, self.checkPositionValidity(matchLineupWithPositions(self.gameID2Home, 'home', self.gameID2Boxscore)))
        self.assertEqual(True, self.checkPositionValidity(matchLineupWithPositions(self.gameID2Away, 'away', self.gameID2Boxscore)))
        self.assertEqual(False, self.checkPositionValidity(matchLineupWithPositions(self.gameID1Home, 'home', {})))


    def checkPositionValidity(self, positions):
        success = True
        if positions:
            for position in positions.values():
                if position not in self.validPositions:
                    success = False
                    break
        else:
            success = False
        return success
