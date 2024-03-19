import logging

import numpy as np
import pandas as pd
from pyrepo_mcda.additions import rank_preferences

from .decision_problem import DecisionProblem
from .utils import plot_correlations_heatmap as static_plot_correlations_heatmap


class Comparison:
    def __init__(self, num_alternatives: int, num_criteria: int):
        self.num_alternatives = num_alternatives
        self.num_criteria = num_criteria

        self.decision_problems = {}
        self.weights_sets = {}

        self.evaluators = {}

        self.scores = {}

        self.correlations = None

    @staticmethod
    def compute_ranks(scores: np.ndarray, is_max_score_best=True):
        ranks = rank_preferences(scores, reverse=True if is_max_score_best else False)
        return ranks

    def add_decision_problem(self, key: str, decision_matrix: np.ndarray, impacts: np.ndarray = None):
        if decision_matrix.shape[0] != self.num_alternatives:
            raise ValueError("Invalid number of alternatives")
        if decision_matrix.shape[1] != self.num_criteria:
            raise ValueError("Invalid number of criteria")

        decision_problem = DecisionProblem(decision_matrix, impacts)
        self.decision_problems[key] = decision_problem

    def add_weights_set(self, key: str, weights):
        self.weights_sets[key] = weights

    def add_evaluator(self, key: str, evaluator):
        self.evaluators[key] = evaluator

    def compute(self, compute_correlations=True) -> None:
        logging.info("Computing scores")
        self.scores = {}

        for decision_problem_key, decision_problem in self.decision_problems.items():
            logging.debug(f"Computing scores for decision problem {decision_problem_key}")
            self.scores[decision_problem_key] = {}

            for weights_set_key, weights_set in self.weights_sets.items():
                logging.debug(f"Computing scores for weights set {weights_set_key}")
                self.scores[decision_problem_key][weights_set_key] = {}

                for evaluator_key, evaluator in self.evaluators.items():
                    logging.debug(f"Computing scores for evaluator {evaluator_key}")
                    scores = evaluator.compute(decision_problem.decision_matrix, weights_set, decision_problem.impacts)
                    self.scores[decision_problem_key][weights_set_key][evaluator_key] = scores

        if compute_correlations:
            logging.info("Computing correlations")
            self.__compute_correlations()

    def to_dataframe(self, normalize_scores: bool = False):
        if len(self.scores) == 0:
            raise ScoresNotComputedError("Scores are not computed yet")

        columns = ["decision_problem", "weights_set", "evaluator", ]
        columns.extend([f"A{i}" for i in range(1, self.num_alternatives + 1)])

        scores_df = pd.DataFrame(columns=columns)
        for decision_problem_key, decision_problem in self.decision_problems.items():
            for weights_set_key, weights_set in self.weights_sets.items():
                for evaluator_key, evaluator in self.evaluators.items():
                    scores = self.scores[decision_problem_key][weights_set_key][evaluator_key]
                    if normalize_scores:
                        normalized_scores = (scores - scores.min()) / (scores.max() - scores.min())
                        row = [decision_problem_key, weights_set_key, evaluator_key, *normalized_scores]
                    else:
                        row = [decision_problem_key, weights_set_key, evaluator_key, *scores]
                    scores_df.loc[len(scores_df)] = row

        return scores_df

    def __compute_correlations(self, method='pearson'):
        if len(self.scores) == 0:
            raise ScoresNotComputedError("Scores are not computed yet")

        logging.debug("Creating correlation matrix")

        scores_df = self.to_dataframe()
        scores_df['label'] = scores_df['decision_problem'] + '-' + scores_df['weights_set'] + '-' + scores_df[
            'evaluator']
        scores_df.set_index('label', inplace=True)
        scores_df = scores_df[scores_df.columns[3:]]
        self.correlations = scores_df.T.corr(method=method)

    def plot_correlations_heatmap(
            self,
            title: str = "Correlation matrix",
            font_scale: float = 0.7,
            labels_format: str = ".4f",
            color_map: str = "YlGnBu",
            x_label: str = "MCDA methods",
            y_label: str = "MCDA methods",
            figure_size: tuple = (16, 9),
    ):
        if self.correlations is None:
            raise ScoresNotComputedError("Correlations are not computed yet")

        plt = static_plot_correlations_heatmap(
            pivot=self.correlations,
            title=title,
            font_scale=font_scale,
            labels_format=labels_format,
            color_map=color_map,
            x_label=x_label,
            y_label=y_label,
            figure_size=figure_size,
        )

        return plt


class ScoresNotComputedError(Exception):
    pass
