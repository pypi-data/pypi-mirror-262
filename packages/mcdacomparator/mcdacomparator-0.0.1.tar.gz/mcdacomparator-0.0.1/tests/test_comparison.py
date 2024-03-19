import unittest

import numpy as np

from comparator.comparison import Comparison, ScoresNotComputedError


class TestComparison(unittest.TestCase):
    def test_compute_ranks_ascending(self):
        scores = np.array([1, 2, 3, 4, 5])
        ranks = Comparison.compute_ranks(scores, is_max_score_best=False)

        self.assertTrue(np.array_equal(ranks, np.array([1, 2, 3, 4, 5])))

    def test_compute_ranks_descending(self):
        scores = np.array([5, 4, 3, 2, 1])
        ranks = Comparison.compute_ranks(scores, is_max_score_best=True)

        self.assertTrue(np.array_equal(ranks, np.array([1, 2, 3, 4, 5])))

    def test_constructor(self):
        comparison = Comparison(3, 3)

        self.assertEqual(comparison.num_alternatives, 3)
        self.assertEqual(comparison.num_criteria, 3)
        self.assertEqual(comparison.decision_problems, {})
        self.assertEqual(comparison.weights_sets, {})
        self.assertEqual(comparison.evaluators, {})
        self.assertEqual(comparison.scores, {})
        self.assertIsNone(comparison.correlations)

    def test_fail_if_not_computed(self):
        comparison = Comparison(3, 3)
        self.assertRaises(ScoresNotComputedError, comparison.to_dataframe)
        self.assertRaises(ScoresNotComputedError, comparison.plot_correlations_heatmap)
