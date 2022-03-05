
class StatisticsClass:
    def __init__(self, expec, npop, table, thres_stat=1.0e-5):
        self.df_expec = expec
        self.df_npop = npop
        self.table = np.nan_to_num(table)
        self.thres_stat = thres_stat

    def run(self):
        self.clean_data()
        self.pairwise_corr()
        self.calc_distances()
        self.plot_preparation()

    def _check_if_significant(data, thresh):
        data_out = data.drop(data.var()[data.var()<thresh].index.values, axis=1)
        indices = data.var()[data.var() > thresh].index.values
        return data_out, indices
    
    def _get_correlation_measure(df):
        drop_values = set() # an unordered collection of items
        cols = df.columns # get the column labels
        print(cols)
        for i in range(0, df.shape[1]):
            for j in range(0, i+1): # get rid of all diagonal entries and the lower triangular
                drop_values.add((cols[i], cols[j]))
        print(drop_values)
        return drop_values
    
    def _euclidean_distance(list_ref, list_comp, vectors):
        distances = np.zeros(len(list_ref))
        for i in range(len(list_ref)):
            distances[i] = np.linalg.norm(vectors[list_comp[i]] - vectors[list_ref[i]])
        return distances

    def clean_data(self):
        self.df_expec2, indices = self._check_if_significant(self.df_expec, self.threshv)
        self.df_npop2, indices_npop = self._check_if_significant(self.df_npop, self.threshv)
        return None

    def pairwise_corr(self):
        df_npop2_short = self.df_npop2.drop(["time"], axis = 1) # get rid of time column
        drop_vals = self._get_correlation_measure(df_npop2_short) # get rid of lower triangular and diagonal entries
        corr2 = df_npop2_short.corr().unstack() # pivot the correlation matrix
        corr2 = corr2.drop(labels=drop_vals).sort_values(ascending=False, key=lambda col: col.abs())
        self.corr2 = corr2
        return None

    def calc_distances(self):
        self.out_dist = self._euclidean_distance([2,4,6],[3,5,7], self.table)
        self.x = range(0,len(self.out_dist))
        return None

    def plot_preparation(self):
        self.df_npop2 = pd.melt(self.df_npop2, ['time'])