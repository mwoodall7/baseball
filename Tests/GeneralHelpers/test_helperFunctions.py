import sys
import unittest

from GeneralHelpers.helperFunctions import getDictItemByKey
from GeneralHelpers.helperFunctions import getCmdOutput


class TestHelperFunctions(unittest.TestCase):

    def setUp(self):
        self.testDict = {'a':1, 'b':2, 'c':3,
                         'd':{'g':5, 'h':6, 'i':7,
                              'j':{'m':10, 'n':11,
                                   'o':{'p':12, 'q':13}
                                   }
                              },
                         'e':{'k':8, 'l':9},
                         'f':4}

        if sys.platform == 'linux':
            self.terminalCommand = 'ls'
        elif sys.platform == 'win32':
            self.terminalCommand = 'dir'

        self.garbageCommand = 'asdf'

################################################################################
# getDictItemByKey - pass in a dictionary that has the potential to have
# numerous subsequent dictionaries and recursively obtain a value for a passed
# in key.
#
# Use Cases:
# 1. Return top level key item
#    - Necessary for recursion
# 2. Get item from subsequent dictionary using recursion
# 3. Return a None value for a desired key that doesn't exist in the dictionary
################################################################################

    def test_getDictItemByKey_topLevelKey(self):
        self.assertEqual(1, getDictItemByKey(self.testDict, 'a'))
        self.assertIsInstance(getDictItemByKey(self.testDict, 'd'), dict)
        self.assertEqual(4, getDictItemByKey(self.testDict, 'f'))


    def test_getDictItemByKey_recursion(self):
        self.assertEqual(5, getDictItemByKey(self.testDict, 'g'))
        self.assertIsInstance(getDictItemByKey(self.testDict, 'j'), dict)
        self.assertEqual(8, getDictItemByKey(self.testDict, 'k'))
        self.assertIsInstance(getDictItemByKey(self.testDict, 'o'), dict)


    def test_getDictItemByKey_keyNotFound(self):
        self.assertEqual(None, getDictItemByKey(self.testDict, 'r'))

################################################################################
# getCmdOutput - obtain the stdout or stderr output from a PC command line call
#
# Use Cases:
# 1. Get the stdout for a general cli command (linux and windows)
# 2. Expect stdout but receive stderr due to an error
# 3. Set getErr to true and obtain stderr output
################################################################################

    def test_getCmdOutput_stdoutDesired(self):
        self.assertIn('stdout:', getCmdOutput(self.terminalCommand, getErr=False))
        self.assertIn('README.md', getCmdOutput(self.terminalCommand, getErr=False))
        self.assertNotIn('stderr:', getCmdOutput(self.terminalCommand, getErr=False))


    def test_getCmdOutput_receiveStderr(self):
        self.assertIn('stderr:', getCmdOutput(self.garbageCommand, getErr=False))
        self.assertIn('not', getCmdOutput(self.garbageCommand, getErr=False))
        self.assertNotIn('stdout:', getCmdOutput(self.garbageCommand, getErr=False))


    def test_getCmdOutput_alwaysReceiveStderr(self):
        self.assertIn('stderr:', getCmdOutput(self.garbageCommand, getErr=True))
        self.assertIn('stderr:', getCmdOutput(self.terminalCommand, getErr=True))
