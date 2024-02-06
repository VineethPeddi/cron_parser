import unittest
from cron_parser import *

class TestCronParser(unittest.TestCase):

    def test_get_minutes(self):
        self.assertEqual(get_minutes("10-12,11,59,0",0,59),[0,10,11,12,59])
        self.assertEqual(get_minutes("*",1,3),[1,2,3])
        self.assertEqual(get_minutes("*/3,5",0,5),[0,3,5])
    def test_get_dates_in_month(self):
        self.assertEqual(get_dates_in_month("*",1,3),[1,2,3])
        self.assertEqual(get_dates_in_month("?",1,3),[])
    def test_get_days_of_week(self):
        self.assertEqual(get_days_of_all_weeks("MON-FRI",0,6), [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
        self.assertEqual(get_days_of_all_weeks("3L",0,6),[[],[],[],[3]])


class TestValidateCronValues(unittest.TestCase):
    def test_valid_cron_values(self):
        # Test with valid cron values
        cron_values = ["*", "*", "*", "*", "*", "cmd"]
        self.assertIsNone(validate_cron_values(cron_values))

    def test_invalid_length(self):
        # Test with invalid length
        cron_values = ["*", "*", "*"]
        with self.assertRaises(ValueError) as context:
            validate_cron_values(cron_values)
        self.assertEqual(str(context.exception), "cron_string must be of length 6")

    def test_invalid_question_mark(self):
        # Test with both day of month and day of week having "?"
        cron_values = ["*", "*", "?", "*", "?", "some-command"]
        with self.assertRaises(ValueError) as context:
            validate_cron_values(cron_values)
        self.assertEqual(str(context.exception), "Both day of month and day of week cannot have ? in a cron expression")

    def test_invalid_multiple_star_values(self):
        # Test with multiple * or L in a cron value
        cron_values = ["1,2,3,*", "*", "*", "*", "*", "*"]
        with self.assertRaises(ValueError) as context:
            validate_cron_values(cron_values)
        self.assertEqual(str(context.exception), "Multiple * are not allowed in a cron value")
    def test_invalid_multiple_L_values(self):
        # Test with multiple * or L in a cron value
        cron_values = ["1,2,3", "*", "L,1", "*", "*", "*"]
        with self.assertRaises(ValueError) as context:
            validate_cron_values(cron_values)
        self.assertEqual(str(context.exception), "Multiple L are not allowed in a cron value")


if __name__ == '__main__':
    unittest.main()
