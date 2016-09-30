from CSFSSelector import CSFSRandomSelector, CSFSBestActualSelector, CSFSBestUncertainSelector

from feature_subset_comparison2 import AUCComparator
import numpy as np
import matplotlib.pyplot as plt

class CSFSEvaluator:

    def __init__(self, df, target):
        self.comparator = AUCComparator(df, target, fast=False, n_folds=2)
        self.df = df
        self.target = target

    def _get_mean_auc_score(self, features):
        return self.comparator.get_mean_score(features)

    def evaluate(self, N_features=5, N_samples=100):
        """

        :param df:
        :param target:
        :param N_features:
        :param N_samples:
        :return: df with auc scores
        """
        random_selector = CSFSRandomSelector(self.df, self.target)
        best_selector = CSFSBestActualSelector(self.df, self.target)
        best_noisy_selector = CSFSBestUncertainSelector(self.df, self.target)

        aucs = {'random': [], 'best': [], 'best_noisy': []}
        for i in range(N_samples):
            random_f = random_selector.select(N_features)
            best_f = best_selector.select(N_features)
            best_noisy_f = best_noisy_selector.select(N_features)

            aucs['random'].append(self._get_mean_auc_score(random_f))
            aucs['best'].append(self._get_mean_auc_score(best_f))
            aucs['best_noisy'].append(self._get_mean_auc_score(best_noisy_f))
        return aucs

    def plot(self, auc_scores, info, show=True):
        """

        :param auc_scores: df mit
        best  best_noisy    random
    0   0.687500    0.718750  0.687500
    1   0.656250    0.718750  0.718750

        :return:
        """
        scores_count = len(auc_scores['best'])
        legend_list = []
        for c in auc_scores:
            mean = np.mean(auc_scores[c])
            std = np.std(auc_scores[c])
            plt.plot(auc_scores[c])
            plt.hold(True)
            plt.plot([mean]*scores_count)
            legend_list.append("{} (std={:.4f})".format(c, std))
            legend_list.append("mean {} ({:.2f})".format(c, mean))
        plt.title('Dataset: {} (using {} features)'.format(info['dataset'], info['N_features']))
        plt.legend(legend_list, loc=4)
        plt.xlabel('# samples (total: {})'.format(scores_count))
        plt.ylabel('AUC')
        if show:
            plt.show()
        fig1 = plt.gcf()
        plt.draw()
        plt.hold(False)
        fig1.savefig('plots/{}/{}features_{}samples.png'.format(info['dataset'], info['N_features'], scores_count), dpi=100)
