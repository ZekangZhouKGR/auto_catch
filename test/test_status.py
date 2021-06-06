import unittest

from auto_catch.hookroute import HookStatus


class Test_HookStatus(unittest.TestCase):

    def test_hookstatus(self):
        a = HookStatus({30, 31})
        b = HookStatus({31, 33})
        c = HookStatus({30, 31})
        self.assertEqual(a, c)
        self.assertNotEqual(a, b)


if __name__ == '__main__':
    unittest.main()