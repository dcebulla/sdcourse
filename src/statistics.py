"""Statistical analysis of data.

This module performs the statistical analysis of the data,
including data cleaning, correlation and distance calculations as
well as preparations for plotting.
"""

import numpy as np
import pandas as pd


class StatisticsClass:
    """Class that performs statistical data analysis.

    Attributes:
        df_expec (dataframe): Dataframe containing expec data.
        df_expec2 (dataframe): Cleaned expec data.
        df_npop (dataframe): Dataframe containing npop data.
        df_npop2 (dataframe): Cleaned npop data.
        table (dataframe):  Dataframe containing table data.
        threshv (float, optional): Threshold variance value for
        data cleaning, default value = 1.0e-5
    """

    def __init__(self, data, thres_stat=1.0e-5):
        """Initializes the class with the required data.

        Note:
            The different parts of data should be named and formatted
            accordingly via the input module.

        Args:
            data (:obj:`InClass`): Contains data for expec, npop and table
            thres_stat (float, optional): Threshold variance value for
        data cleaning, default value = 1.0e-5

        """
        self.df_expec = data.expec
        self.df_npop = data.npop
        self.table = np.nan_to_num(data.table)
        self.threshv = thres_stat

    def run(self):
        """Runs methods neccessary for statistical data analysis"""
        self.clean_data()
        self.pairwise_corr()
        self.calc_distances()
        self.plot_preparation()

    def _check_if_significant(self, data, thresh):
        """Helper method to check significances of variables.

        Note:
            Used for expec and npop data.

        Args:
            data (dic): Data for which significance is checked and where
            data is droppd if it is not significant.
            thresh (float): Threshold used to check significance.
        """
        data_out = data.drop(
            data.var()[data.var() < thresh].index.values, axis=1
        )
        indices = data.var()[data.var() > thresh].index.values
        return data_out, indices

    def _get_correlation_measure(self, df):
        """Helper method to calculate correlation.

        Note:
            Used for npop data.

        Args:
            df (dataframe): Data for which correlation is calculated.
        """
        drop_values = set()  # an unordered collection of items
        cols = df.columns  # get the column labels
        print(cols)
        for i in range(0, df.shape[1]):
            for j in range(
                0, i + 1
            ):  # get rid of all diagonal entries and the lower triangular
                drop_values.add((cols[i], cols[j]))
        print(drop_values)
        return drop_values

    def _euclidean_distance(self, list_ref, list_comp, vectors):
        """Helper method to calculate euclidean distances.

        Note:
            Used for table data.

        Args:
            list_ref (list): List of reference vectors
            list_comp (list): List of vectors that are compared to
            reference vectors
            vectors (list): List of vector data
        """
        distances = np.zeros(len(list_ref))
        for i in range(len(list_ref)):
            distances[i] = np.linalg.norm(
                vectors[list_comp[i]] - vectors[list_ref[i]]
            )
        return distances

    def clean_data(self):
        """Cleans expec and npop data based on significance"""

        # TODO: Handle invalid thresv values

        self.df_expec2, indices = self._check_if_significant(
            self.df_expec, self.threshv
        )
        self.df_npop2, indices_npop = self._check_if_significant(
            self.df_npop, self.threshv
        )
        return None

    def pairwise_corr(self):
        """Calculates pairwise correlations in cleaned npop data"""
        df_npop2_short = self.df_npop2.drop(
            ["time"], axis=1
        )  # get rid of time column
        drop_vals = self._get_correlation_measure(
            df_npop2_short
        )  # get rid of lower triangular and diagonal entries
        corr2 = df_npop2_short.corr().unstack()  # pivot the correlation matrix
        corr2 = corr2.drop(labels=drop_vals).sort_values(
            ascending=False, key=lambda col: col.abs()
        )
        self.corr2 = corr2
        return None

    def calc_distances(self):
        """Calculates distances of specified vectors in table data."""
        self.out_dist = self._euclidean_distance(
            [2, 4, 6], [3, 5, 7], self.table
        )
        self.x = range(0, len(self.out_dist))
        return None

    def plot_preparation(self):
        """Melts cleaned npop data from wide to long format for plotting"""
        self.df_npop2 = pd.melt(self.df_npop2, ["time"])
