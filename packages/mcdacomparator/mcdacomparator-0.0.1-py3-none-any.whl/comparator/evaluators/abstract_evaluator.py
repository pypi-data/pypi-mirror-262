import numpy as np


class AbstractEvaluator:
    def compute(self, decision_matrix: np.ndarray, weights: np.ndarray, impacts: np.ndarray) -> np.ndarray:
        """
        Computes the scores for alternatives based on decision matrix, weights and impacts.

        Parameters:
            `decision_matrix` (np.ndarray): Decision matrix, indexed first by alternatives, and then by criterial performances.
            `weights` (np.ndarray): A vector of weights for each criterion.
            `impacts` (np.ndarray): A vector of impacts for each criterion. `+1` as benefit, `-1` as cost.

        Returns:
            np.ndarray: Result scores as np.ndarray vector (one value for each alternative).

        """
        raise NotImplementedError("You need to override this method in your non-abstract evaluator")
