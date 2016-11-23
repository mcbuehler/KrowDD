import numpy as np
import pandas as pd
import re

import sys

from sklearn.preprocessing import Imputer
from tabulate import tabulate

from CSFSCrowdCleaner import CSFSCrowdAggregator, CSFSCrowdAnalyser, CSFSCrowdCleaner
from CSFSDataPreparator import DataPreparator
from CSFSEvaluator import CSFSEvaluator
from CSFSSelector import CSFSBestActualSelector, CSFSBestFromMetaSelector
from abstract_experiment import AbstractExperiment
from infoformulas_listcomp import _H, IG_from_series, H
from util.util_features import get_feature_inf, get_features_from_questions


class ExperimentStudent(AbstractExperiment):

    def __init__(self, dataset_name, experiment_number, experiment_name):
        super().__init__(dataset_name, experiment_number, experiment_name)

        self.path_raw = '{}raw/{}/student-por.csv'.format(self.base_path, experiment_name)
        self.path_cleaned = '{}cleaned/{}/student-por_clean.csv'.format(self.base_path, experiment_name)
        self.path_bin = '{}cleaned/{}/student-por_clean_bin.csv'.format(self.base_path, experiment_name)
        self.path_meta = '{}cleaned/{}/student-por_clean_bin_meta.csv'.format(self.base_path, experiment_name)
        # self.path_answers_raw = '{}results/{}/answers_raw.xlsx'.format(base_path, experiment_name)
        # self.path_answers_clean = '{}results/{}/answers_clean.csv'.format(base_path, experiment_name)
        # self.path_answers_aggregated = '{}results/{}/answers_aggregated.csv'.format(base_path, experiment_name)
        # self.path_answers_metadata = '{}results/{}/answers_metadata.csv'.format(base_path, experiment_name)
        # self.path_csfs_auc = '{}results/{}/csfs_auc.csv'.format(base_path, experiment_name)
        # self.path_questions = '{}questions/{}/questions.csv'.format(base_path, experiment_name) # experiment2 for experiment3
        # self.path_flock_result = '{}questions/{}/flock_auc.csv'.format(experiment_name)
        self.target = 'G3'


    def preprocess_raw(self):
        """
        Selects only interesting features, fills gaps
        outputs a csv into "cleaned" folder
        :return:
        """
        df_raw = pd.read_csv(self.path_raw, quotechar='"', delimiter=';')

        features_to_remove = ['G1', 'G2']
        preparator = DataPreparator()

        # only take subset we have questions for
        df_raw = preparator.prepare(df_raw, features_to_remove, no_bins=3, columns_to_ignore=['G3'])
        df_raw.to_csv(self.path_cleaned, index=False)

    def bin_binarise(self):
        """
        binning and binarise
        outputs a csv into "cleaned" folder "_bin"
        :return:
        """

        """
        binning and binarise
        outputs a csv into "cleaned" folder "_bin"
        :return:
        """
        df = pd.read_csv(self.path_cleaned)
        target_median = np.median(df[self.target])

        df[self.target] = df[self.target].apply(lambda x: 1 if x >= target_median else 0) # 1:"belongs to the better one" 0: "belongs to the lower half or middle"

        preparator = DataPreparator()
        df = preparator.prepare(df, columns_to_ignore=[self.target])
        df.to_csv(self.path_bin, index=False)

    def _get_dataset_bin(self):
        """
        Selects subset of data set we have questions for.
        """
        pass

    def evaluate_crowd_all_answers(self):
        """
        Aggregates crowd answers and evaluates for all crowd answers
        :return:
        """
        pass


    def evaluate_csfs_auc(self):
        pass


    def evaluate_flock(self):
        pass


if __name__ == '__main__':
    experiment = ExperimentStudent('student', 2, 'experiment2_por')
    # experiment.set_up_basic_folder_structure()
    # experiment.set_up_experiment_folder_structure('experiment2_por')
    experiment.preprocess_raw()
    experiment.bin_binarise()
    experiment.get_metadata()
    # experiment.evaluate_crowd_all_answers()
    # experiment.evaluate_flock()
    # experiment.evaluate_csfs_auc()