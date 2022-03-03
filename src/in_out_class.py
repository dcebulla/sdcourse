import pandas as pd
import numpy as np


class InClass:
    def __init__(self, data_path="data/"):
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
            # Statistics
            "expec.t": lambda path: pd.read_csv(path, r"\s+"),
            "npop.t": lambda path: pd.read_csv(path, r"\s+"),
            "table.dat": lambda path: np.loadtxt(path, skiprows=1).T,
            # Numerics:
            "efield.t": lambda path: np.loadtxt(path, skiprows=1),
            "nstate_i.t": lambda path: np.loadtxt(path, skiprows=1),
        }

        # map file names to class attributes
        self.names_to_attributes = {
            # Statistics
            "expec.t": "expec",
            "npop.t": "npop",
            "table.dat": "table",
            # Numerics:
            "efield.t": "efield",
            "nstate_i.t": "nstate_i",
        }

    def read_data(
        self,
        file_names=[
            "expec.t",
            "npop.t",
            "table.dat",
            "efield.t",
            "nstate_i.t",
        ],
    ):
        # This function reads all the files whose names are given as input
        for name in file_names:
            full_path = self.data_path + name
            vars(self)[self.names_to_attributes[name]] = self.read_functions[
                name
            ](full_path)

    def read_statistics_data(self):
        # for convenience, this call read_data only w. the files for statistics
        self.read_data(file_names=["expec.t", "npop.t", "table.dat"])

    def read_numerics_data(self):
        # for convenience, this call read_data only with the files for numerics
        self.read_data(file_names=["efield.t", "nstate_i.t"])


class OutClass:
    def __init__(self, savepdf=False):
        self.savepdf = savepdf  # flag whether to save things as pdf
