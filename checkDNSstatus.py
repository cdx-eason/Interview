from BaseClass import BaseClass
from Config import Config

import unittest


class SampleTest(unittest.TestCase):
    def setUp(self):
        print '\ntest start'

    def tearDown(self):
        print '\ntest stop'

    def test_check_dns(self):
        bc = BaseClass()
        self.assertEqual(bc.callwithhttplib(), 200, bc.queryresponse)
        bc.isrunwithjsonfile()  # check if continue with system.cfg -> test_json_file
        self.assertIsNotNone(bc.convertjson(bc.data), 'Invalid Response:\n' + bc.data)
        self.assertTrue(bc.parsejson(bc.objjson), 'Invalid Json:\n' + bc.data)
        self.assertTrue(bc.overallstatus, Config.readdnserror())


if __name__ == '__main__':
    unittest.main()