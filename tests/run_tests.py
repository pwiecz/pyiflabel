# Code taken from:
# http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure


import unittest
import all_tests
import sys
import os


sys.path.insert(1, os.path.abspath(".."))
testSuite = all_tests.create_test_suite()
text_runner = unittest.TextTestRunner().run(testSuite)
