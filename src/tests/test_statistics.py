import pandas as pd
import numpy as np
from statistics import StatisticsClass
from in_out_class import InClass


data = InClass()
stats = StatisticsClass(data)


def test_clean_data():

    stats.df_expec = pd.DataFrame({1.0: [10, 100], 2.0: [1, 1]})
    expec_cleaned = pd.DataFrame({1.0: [10, 100]})

    stats.df_npop = pd.DataFrame({1.0: [10, 100], 2.0: [1, 1]})
    npop_cleaned = pd.DataFrame({1.0: [10, 100]})

    stats.clean_data()

    assert stats.df_expec2.equals(expec_cleaned)
    assert stats.df_npop2.equals(npop_cleaned)
    # TODO: Tests for invalid thresv values


def test_calc_distances():
    stats.table = np.array(
        [
            [1, 2, 1],
            [1, 1, 3],
            [1, 0, 3],
            [1, 4, 3],
            [1, 2, 3],
            [2, 1, 3],
            [3, 1, 3],
            [0, 1, 3],
        ]
    )

    true_dist = np.array([4.0, np.sqrt(2), 3.0])
    true_x = range(0, 3)

    stats.calc_distances()

    assert np.array_equal(stats.out_dist, true_dist)
    assert stats.x == true_x


# Sorry, I have no idea how to create a Pandas series
#  that is equal to the result
# def test_pairwise_corr():

#     stats.df_npop2 = pd.DataFrame({"time": [10, 100],
#  "Time": [1, 1], "Test": [-1, 1]})
#     # npop2_cleaned = pd.DataFrame({2.0: [1, 1]})

#     stats.pairwise_corr()

#     assert stats.df_npop2_short.equals(npop2_cleaned)
