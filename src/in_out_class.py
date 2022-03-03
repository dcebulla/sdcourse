import pandas as pd
import numpy as np


class InClass:
    def __init__(self, data_path="../data/"):
        self.data_path = data_path  # general data path

        # statistics related data fields
        self.expec = None
        self.npop = None
        self.table = None

        # numerics related data fields
        self.efield = None
        self.nstate_i = None

        # define methods to read
        self.read_functions = {
            "expec.t": lambda path: pd.read_csv(path, r"\s+"),
            "npop.t": lambda path: pd.read_csv(path, r"\s+"),
            "table.dat": lambda path: np.loadtxt(path, skiprows=1).T,
            # Numerics:
            "efield.t": lambda path: np.loadtxt(path, skiprows=1),
            "nstate_i.t": lambda path: np.loadtxt(path, skiprows=1),
        }

    # def read_statistics_data(
    #     self,
    #     file_names = ["expec.t, npop.t, table.dat"]):
    #     self.


class OutClass:
    def __init__(self, savepdf=False):
        self.savepdf = savepdf  # flag whether to save things as pdf
