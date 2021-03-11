'''
Copyright © Matthew Woodall (mwoodall7 on Github). All Worldwide Rights Reserved.
This material is the property of Matthew Woodall a.k.a. sparePartsBud on Github.
All use, alterations, disclosure, dissemination, and/or reproduction not specifically
authorized by sparePartsBud is prohibited.
'''
from datetime import datetime

import os
import sys
import time
import unittest

# Required to update PYTHONPATH for runner to have access to classes within project
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'GeneralHelpers'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Application'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Tests'))

from GeneralHelpers.RecordKeeper import RecordKeeper


def discoverTestSuites():
    suites = {}
    for dirPath, dirNames, fileNames in os.walk(os.path.join(os.getcwd(), 'Tests')):
        if dirPath not in suites:
            suites[dirPath] = []
        for file in fileNames:
            if file.startswith('test_'):
                suites[dirPath].append(file)
    return suites


def importTestSuiteModules(suiteDirPath, tests):
    sys.dont_write_bytecode = True
    moduleList = []
    if suiteDirPath not in sys.path:
        sys.path.append(os.path.join(suiteDirPath))
    for test in tests:
        testName, _unused_ext = os.path.splitext(test)
        moduleList.append(__import__(testName))
    del sys.path[-1]
    return moduleList


def runTestSuite(testModules, streamFile):
    testLoader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for test in testModules:
        suite.addTests(testLoader.loadTestsFromModule(test))

    testRunner = unittest.TextTestRunner(stream=streamFile, verbosity=3)
    suiteResults = testRunner.run(suite)
    return suiteResults



def main():
    resultDir = os.path.join(os.getcwd(), 'TestResults')
    if not os.path.exists(resultDir):
        os.mkdir(resultDir)
    testRecordKeeper = RecordKeeper(resultDir, daysToKeep=30)
    print("Checking for old test results to remove from system...")
    testRecordKeeper.processRecords()
    print('\n')

    testStartTime = datetime.now()

    resultFileName = f'unitTestResults_{testStartTime.year}_{testStartTime.month}_{testStartTime.day}_{testStartTime.hour}_{testStartTime.minute}_{testStartTime.second}.log'

    resultFile = open(os.path.join(resultDir, resultFileName), 'w+')
    resultFile.write('**************************************************\n' +
                     f'{datetime.today()} - Unit Test Results\n' +
                     '**************************************************\n')

    suiteResults = {}

    testRunTimeStart = time.time()
    testSuites = discoverTestSuites()
    for suiteDir, testList in testSuites.items():
        if testList:
            suiteName = os.path.basename(suiteDir)
            resultFile.write('\nTest Suite: {}\n\n'.format(suiteName))
            suiteModules = importTestSuiteModules(suiteDir, testList)
            suiteResults[suiteName] = runTestSuite(suiteModules, resultFile)
    testTimeElapse = time.time() - testRunTimeStart

    if all([suiteResult.wasSuccessful() for suiteResult in suiteResults.values()]):
        print(f"All tests PASSED! Run Time: {testTimeElapse:.3f} sec")
    else:
        print(f"FAIL. Check log file in TestResults directory for specific failure information: {resultFileName}.\nRun Time: {testTimeElapse:.3f} sec")

    resultFile.close()


if __name__ == '__main__':
    main()
