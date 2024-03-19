import unittest

import numpy as np

from comparator.decision_problem import DecisionProblem


class TestDecisionProblem(unittest.TestCase):
    def test_raise_when_mismatch_count_of_criteria_and_impacts(self):
        dm = np.array([[10, 10, 10], [20, 10, 10], [10, 30, 10]])
        impacts = np.array([1, 1])

        self.assertRaises(ValueError, DecisionProblem, dm, impacts)

    def test_no_error_when_match_count_of_criteria_and_impacts(self):
        dm = np.array([[10, 10, 10], [20, 10, 10], [10, 30, 10]])
        impacts = np.array([1, 1, 1])

        dp = DecisionProblem(dm, impacts)
        self.assertTrue(np.array_equal(dp.decision_matrix, dm))
        self.assertTrue(np.array_equal(dp.impacts, impacts))
