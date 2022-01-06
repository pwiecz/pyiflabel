# Code taken from:
# http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure

import glob
import unittest

def create_test_suite():
    test_file_strings = glob.glob('test_*.py')
    test_file_strings.remove('test_storyformat.py')
    module_strings = [str[:len(str)-3] for str in test_file_strings]
    suites = [unittest.defaultTestLoader.loadTestsFromName(name) \
              for name in module_strings]
    testSuite = unittest.TestSuite(suites)
    return testSuite
