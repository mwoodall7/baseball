'''
Copyright © Matthew Woodall (mwoodall7 on Github). All Worldwide Rights Reserved.
This material is the property of Matthew Woodall a.k.a. mwoodall7 on Github.

All use, alterations, disclosure, dissemination, and/or reproduction not specifically
authorized by sparePartsBud is prohibited.
'''
import sys

import unittest
import statsapi
from datetime import date

from Application.GenerateData.GenerateData import getWinLossRecords
from Application.GenerateData.GenerateData import getLineupIds
from Application.GenerateData.GenerateData import matchLineupWithPositions
from Application.GenerateData.GenerateData import getPositionPlayerData
from Application.GenerateData.GenerateData import getBattingData
from Application.GenerateData.GenerateData import getPitcherData
from Application.GenerateData.GenerateData import appendValidData

OPENING_DAY = date(year=2021, month=4, day=1)


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

        # These values are going to need to be focused on length and datatype
        # over exact values as the career stats will update with new games
        self.AdamWainwrightID = 425794
        self.AdamWainwrightData = statsapi.player_stat_data(personId=self.AdamWainwrightID, type='career')
        self.AdamWainwrightPitching = ['393', '326', '2597', '1933', '876', '428', '38', '176', '1830', '591', '36', '2066', '64', '.252', '8200', '.306', '1.098', '1.403', '41', '56', '.577', '216', '33583', '3.38', '2169.1', '167', '98', '3', '5', '17', '815', '1.22', '9001', '393', '24', '10', '21585', '64.3', '64', '3', '41', '4', '1.34', '.630', '15.5', '13', '3.10', '7.59', '2.45', '8.57', '5.29', '0.73', '15', '4', '96', '50']
        self.AdamWainwrightHitting = ['391', '247', '149', '54', '37', '2', '10', '224', '24', '0', '136', '0', '.199', '685', '.225', '.302', '.527', '2', '0', '.000', '9', '2610', '772', '207', '71', '338', '60', '3', '.278', '1.66', '68.50']
        self.AdamWainwrightFielding = ['280', '191', '8', '479', '.983', '1.20', '2169.1', '393', '326', '26']
        self.AdamWainwrightPositionData = self.AdamWainwrightHitting.copy()
        for stat in self.AdamWainwrightFielding:
            self.AdamWainwrightPositionData.append(stat)

        self.TylerONeillID = 641933
        self.TylerONeillData = statsapi.player_stat_data(personId=self.TylerONeillID, type='career')
        self.TylerONeillHitting = ['171', '65', '101', '67', '16', '0', '21', '153', '32', '0', '94', '5', '.229', '410', '.291', '.422', '.713', '1', '6', '.857', '6', '1802', '450', '173', '58', '195', '0', '3', '.305', '0.64', '19.52']
        self.TylerONeillFieldingLF = ['1', '149', '3', '153', '.980', '1.55', '701.0', '97', '80', '0']
        self.TylerONeillFieldingCF = ['0', '7', '1', '8', '.875', '1.17', '43.2', '6', '6', '0']
        self.TylerONeillPositionData = self.TylerONeillHitting.copy()
        self.TylerONeillNewPositionData = self.TylerONeillHitting.copy()
        for stat in self.TylerONeillFieldingLF:
            self.TylerONeillPositionData.append(stat)
            self.TylerONeillNewPositionData.append('0')


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

################################################################################
# getPositionPlayerData - pass in the player data and position and return a list
# of strings representing the hitting and then fielding stats for a player a the
# specified position.
#
# Use Cases:
# 1. valid player data returns the hitting and fielding data in a single list
# 2. invalid player data returns an empty list
# 3. position required not present in list returns a list of 0's since it would
#    be the first time the player is starting in that fielding position
#
################################################################################

    @unittest.skipIf(date.today() >= OPENING_DAY, "2021 season has started. Career stats are now dynamic.")
    def test_getPositionPlayerData_validPlayerData(self):
        self.assertEqual(self.AdamWainwrightPositionData, getPositionPlayerData(self.AdamWainwrightData, 'P'))
        self.assertEqual(self.TylerONeillPositionData, getPositionPlayerData(self.TylerONeillData, 'LF'))


    def test_getPositionPlayerData_validPlayerDataSize(self):
        self.assertEqual(41, len(getPositionPlayerData(self.AdamWainwrightData, 'P')))
        self.assertEqual(41, len(getPositionPlayerData(self.TylerONeillData, 'LF')))


    def test_getPositionPlayerData_invalidData(self):
        self.assertEqual([], getPositionPlayerData({}, 'P'))
        self.assertEqual([], getPositionPlayerData({'stuff': None}, 'C'))
        self.assertEqual([], getPositionPlayerData({'stats': None}, 'LF'))


    @unittest.skipIf(date.today() >= OPENING_DAY, "2021 season has started. Career stats are now dynamic.")
    def test_getPositionPlayerData_neededPositionMissing(self):
        self.assertEqual(self.TylerONeillNewPositionData, getPositionPlayerData(self.TylerONeillData, 'C'))

################################################################################
# getBattingData - pass in the player data and return a list of the strings
# representing the hitting data for the player
#
# Use Cases:
# 1. valid player data returns the hitting data in a single list
# 2. invalid player data returns an empty list
#
################################################################################

    @unittest.skipIf(date.today() >= OPENING_DAY, "2021 season has started. Career stats are now dynamic.")
    def test_getBattingData_validPlayerData(self):
        self.assertEqual(self.AdamWainwrightHitting, getBattingData(self.AdamWainwrightData))
        self.assertEqual(self.TylerONeillHitting, getBattingData(self.TylerONeillData))


    def test_getBattingData_validPlayerDataSize(self):
        self.assertEqual(31, len(getBattingData(self.AdamWainwrightData)))
        self.assertEqual(31, len(getBattingData(self.TylerONeillData)))


    def test_getBattingData_invalidData(self):
        self.assertEqual([], getBattingData({}))
        self.assertEqual([], getBattingData({'stuff':None}))
        self.assertEqual([], getBattingData({'stats': None}))

################################################################################
# getPitcherData - pass in the player data and return a list of the strings
# representing the pitching data for the player
#
# Use Cases:
# 1. valid player data returns the pitching data in a single list
# 2. invalid player data returns an empty list
#
################################################################################

    @unittest.skipIf(date.today() >= OPENING_DAY, "2021 season has started. Career stats are now dynamic.")
    def test_getPitcherData_validPlayerData(self):
        self.assertEqual(self.AdamWainwrightPitching, getPitcherData(self.AdamWainwrightData))


    def test_getPitcherData_validPlayerDataSize(self):
        self.assertEqual(56, len(getPitcherData(self.AdamWainwrightData)))
        self.assertEqual(0, len(getPitcherData(self.TylerONeillData)))


    def test_getPlayerData_invalidData(self):
        self.assertEqual([], getPitcherData(self.TylerONeillData))
        self.assertEqual([], getPitcherData({}))
        self.assertEqual([], getPitcherData({'stuff':None}))
        self.assertEqual([], getPitcherData({'stats':None}))

################################################################################
# appendValidData - pass in the list to append data to and the value to append
#
# Use Cases:
# 1. value is a valid string representation of a numeric value
# 2. value is not numeric
#
################################################################################

    def test_appendValidData_validNumericValue(self):
        dataList = []
        appendValidData(dataList, '10')
        self.assertEqual(['10'], dataList)
        appendValidData(dataList, '0')
        self.assertEqual(['10', '0'], dataList)
        appendValidData(dataList, '0.456')
        self.assertEqual(['10', '0', '0.456'], dataList)
        appendValidData(dataList, '12345')
        self.assertEqual(['10', '0', '0.456', '12345'], dataList)


    def test_appendValidData_nonNumericValue(self):
        dataList = []
        appendValidData(dataList, '-.--')
        self.assertEqual(['0'], dataList)
        appendValidData(dataList, 'stuff')
        self.assertEqual(['0', '0'], dataList)
        appendValidData(dataList, 'NotANumber1234')
        self.assertEqual(['0', '0', '0'], dataList)
