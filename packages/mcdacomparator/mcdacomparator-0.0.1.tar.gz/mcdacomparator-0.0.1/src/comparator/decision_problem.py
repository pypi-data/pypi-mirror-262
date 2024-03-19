import numpy as np


class DecisionProblem:
    """
    Class representing the decision problem. Contains the non-normalized decision matrix with
     criterial performances of each alternative and impacts of each criterion (benefit or cost).

    Attributes:
        decision_matrix (np.ndarray): A n x m array of n alternatives and their m criterial performances.
        impacts (np.ndarray): A m-sized array of impacts of criteria - +1 for benefit and -1 for cost.
    """

    def __init__(self, decision_matrix: np.ndarray, impacts: np.ndarray = None) -> None:
        """
        :param decision_matrix: A n x m array of n alternatives and their m criterial performances.
        :param impacts: A m-sized array of impacts of criteria - +1 for benefit and -1 for cost.
        """
        self.decision_matrix = decision_matrix

        if impacts is None:
            self.impacts = np.ones(decision_matrix.shape[1])
        else:
            self.impacts = impacts

        if decision_matrix.shape[1] != impacts.shape[0]:
            raise ValueError(f"There are {impacts.shape[0]} impacts but {decision_matrix.shape[1]} criteria")
