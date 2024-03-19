import numpy as np
from pyrepo_mcda.distance_metrics import euclidean as euclidean_distance
from pyrepo_mcda.mcda_methods import TOPSIS
from pyrepo_mcda.normalizations import vector_normalization

from .abstract_evaluator import AbstractEvaluator


class TopsisEvaluator(AbstractEvaluator):

    def compute(self, decision_matrix: np.ndarray, weights: np.ndarray, impacts: np.ndarray) -> np.ndarray:
        topsis = TOPSIS(normalization_method=vector_normalization, distance_metric=euclidean_distance)
        ccis = topsis(decision_matrix, weights, impacts)

        return ccis
