import Assignment1SalesApp.py
import unittest

class MyTest(unittest.TestCase):
    """Testing loadData_Bad.txt and whether it is loading into the
    Model class correctly via get_data"""
    def test1(self):
        #rawdata = 'a0111', should be None ~~ too long
        self.assertEqual(id_list[1], None)

    def test2(self):
        #rawdata = '?', should be None ~~ invalid char
        self.assertNotEqual(gender_list[1], None)

    def test3(self):
        #rawdata = 'u', should be uppercase "U" ~~ invalid char
        self.assertEqual(bmi_list[1[1]], "U")

    def test4(self):
         # rawdata = " ", should be None ~~ no data entered
        self.assertEqual(income_list[3], None)

    def test5(self):
        #rawdata = 'F', should be 'F' ~~ valid char
        self.assertEqual(gender_list[5], "F")

    def test6(self):
        #raw_data = " ", should be None ~~ no data entered
        self.assertEqual(bmi_list[4], None)

if __name__ == '__main__':
    unittest.main() #runs the tests

