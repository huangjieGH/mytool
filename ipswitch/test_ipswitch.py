import unittest
import ipswitch

class TestIpswitch(unittest.TestCase):

    def setUp(self):
        self.normal_inargs = ['inner','outer']
        self.abnormal_inargs = ['hello']

    def tearDown(self):
        pass

    def test_switchNetworkConfiguration(self):
        self.assertTrue(ipswitch.switchNetworkConfiguration(self.normal_inargs[0]))
        self.assertTrue(ipswitch.switchNetworkConfiguration(self.normal_inargs[1]))
        self.assertFalse(ipswitch.switchNetworkConfiguration(self.abnormal_inargs[0]))

if __name__ == '__main__':
    unittest.main()
