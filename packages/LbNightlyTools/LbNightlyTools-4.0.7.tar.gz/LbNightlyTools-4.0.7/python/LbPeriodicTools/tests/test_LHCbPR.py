###############################################################################
# (c) Copyright 2013 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""

Test for the PeriodTest Tools

Created on Dec 3, 2013

@author: Ben Couturier
"""
from __future__ import print_function

import json
import logging
import os
import unittest
from os.path import join, normpath

from LbPeriodicTools.LbPeriodicStarter import PeriodicTestStarter


class Test(unittest.TestCase):
    """Test case of the PeriodicTestStarter class"""

    def setUp(self):
        """Setup the test"""
        self._data_dir = normpath(
            join(*([__file__] + [os.pardir] * 4 + ["testdata", "periodic_tests"]))
        )
        self._data_file = join(self._data_dir, "lhcbpr_schedule.xml")
        self._json_file = join(self._data_dir, "slotbuilds.json")
        self._slot_data = None
        with open(self._json_file) as jsonfile:
            self._slot_data = json.load(jsonfile)

        logging.basicConfig(level=logging.INFO)

    def tearDown(self):
        """tear down the test"""
        pass

    def testLHCbPR(self):
        """
        Test the PeriodicTestStarter based on the saved JSON file
        """
        starter = PeriodicTestStarter(
            self._data_file, "2013-12-02", 86400, lambda x: self._slot_data
        )
        all_tests = starter.getAllTests()
        for t in all_tests:
            for tt in t[1]:
                print(tt)

        self.assertEqual(len(all_tests), 2, "2 Matches")
        # we should have below 2 and 1 tests matching, respectively
        # but because of 3cbd9676 we need to take into account that dummy slot data
        # do not contain info about slot date
        self.assertEqual(len(all_tests[0][1]), 4, "Tests matching for 4 configs")
        self.assertEqual(len(all_tests[1][1]), 2, "Tests matching for 2 configs")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testLoadXML']
    unittest.main()
