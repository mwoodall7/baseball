import sys
import unittest

from Application.GenerateData.GenerateData import getWinLossRecords
from Application.GenerateData.GenerateData import getLineupIds


class TestGenerateData(unittest.TestCase):

    def setUp(self):
        self.testDateStandingsFormat = '08/15/2020'
        self.testHomeIdWL = 133
        self.testAwayIdWL = 146

        self.gameIDLineups = 631508

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
# getLineupIds - pass in the game ID and return the player IDs in list format
# for the home and away teams. Each list should contain 10 player IDs for
# the 9 players batting, and the starting pitcher's ID.
#
# Use Cases:
# 1. Get the player IDs for both teams with the given game ID
# 2. Invalid game ID passed in
#
################################################################################

    def test_getLineupIds_validGame(self):
        homeLineup = [641313, 660162, 518735, 547989, 429665, 650391, 673357, 608577, 664901, 608337]
        awayLineup = [543939, 669242, 502671, 641933, 572761, 666185, 451594, 668800, 664056, 425794]
        checkHomeLineup, checkAwayLineup = getLineupIds(self.gameIDLineups)
        self.assertEqual(homeLineup, checkHomeLineup)
        self.assertEqual(awayLineup, checkAwayLineup)


    def test_getLineupIds_invalidGame(self):
        checkHomeLineup, checkAwayLineup = getLineupIds(0)
        self.assertEqual(None, checkHomeLineup)
        self.assertEqual(None, checkAwayLineup)
