"""
This module provides the classes InClass and OutClass.

From this module one can import the classes InClass and OutClass.
The class InClass allows to create objects that read in the data.
The class OutClass allows to create objects that output the results.

Required Packages:
    - pandas
    - numpy
    - matplotlib.pyplot
    - seaborn

Provides:
    - InClass
    - OutClass
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn


class InClass:
    """
    Class for reading the data.

    Objects of the InClass read the data files in a given path.
    You can either read all files at once using read_data with
    the default option or read the numerics and statistics part
    seperately using read_statistics and read_numerics or you
    can define which files to read by passing a list of the file
    names to read_data.

    Args:
        data_path (str): (Relative) Path of the directory with the
            data files.
            Default: "data/"

    Attributes:
        data_path (str):  (Relative) Path of the directory with the
            data files.
        expec (none or pandas dataframe): Data of the expec.t file
        npop (none or pandas dataframe): Data of the npop.t file
        table (none or numpy array): Data of the table.dat file
        efield (none or numpy array): Data of the efield.t file
        nstate_i (none or numpy array): Data of the nstate_i.t file
        read_functions (dict): Dictionary that maps file name to
            suitable tailored reader function
        names_to_attributes (dict): Dictionary that maps file names to
            class attributes
    """

    def __init__(self, data_path="data/"):
        """Initialize the object

        Args:
            data_path (str): (Relative) Path of the directory with the
                data files.
                Default: "data/"
        """
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
        """
        Reads all the files whose names are given as input.

        Args:
            file_names (list of str): List of file names.
                Default: file_names=[
                "expec.t",
                "npop.t",
                "table.dat",
                "efield.t",
                "nstate_i.t",
                ]
        """
        for name in file_names:
            full_path = self.data_path + name
            vars(self)[self.names_to_attributes[name]] = self.read_functions[
                name
            ](full_path)

    def read_statistics_data(self):
        """
        Calls read_data with file names that correspond to statistics.

        The relevant file names are ["expec.t", "npop.t", "table.dat"]

        """

        self.read_data(file_names=["expec.t", "npop.t", "table.dat"])

    def read_numerics_data(self):
        """
        Calls read_data with file names that correspond to numerics.

        The relevant file names are ["efield.t", "nstate_i.t"]

        """

        self.read_data(file_names=["efield.t", "nstate_i.t"])


class OutClass:
    """
    Class for outputting the results.

    Based on a statistics and a numerics object the OutClass creates
    objects which provide functions to plot relevant plots and save
    relevant results. Plots can be saved to files, too.

    Args:
        statistics (object of StatisticsClass): Object of
            StatisticsClass which contains the results of the
            statistical analysis.
        numerics (object of NumericsClass): Object of
            NumericsClass which contains the results of the
            statistical analysis.
        savepdf (bool): Flag whether the plots should be saved to PDF
            files (True) or not (False). Default: False
        write_out (bool): Flag whether the results should be saved in
            files (True) or not (False). Default: False

    Attributes:
        statistics (object of StatisticsClass): Object of
            StatisticsClass which contains the results of the
            statistical analysis.
        numerics (object of NumericsClass): Object of
            NumericsClass which contains the results of the
            statistical analysis.
        savepdf (bool): Flag whether the plots should be saved to PDF
            files (True) or not (False). Default: False
        write_out (bool): Flag whether the results should be saved in
            files (True) or not (False). Default: False
    """

    def __init__(self, statistics, numerics, savepdf=False, write_out=False):

        self.statistics = statistics
        self.numerics = numerics
        self.savepdf = savepdf
        self.write_out = write_out

    def plot_statistics(self):
        """
        Plot all statistic plots. Possibly save them.

        The plots will be displayed in the main notebook. Depending on
        the flag savepdf, the plots are also saved to pdf files.
        """

        # Task 1
        sn.relplot(
            data=self.statistics.df_expec, kind="line", x="time", y="<z>"
        )
        plt.show()

        sn.pairplot(self.statistics.df_expec, corner=True)
        plt.show()

        # Task 2
        sn.pairplot(self.statistics.df_expec2, corner=True)
        if self.savepdf:
            plt.savefig(
                "task2_relevant_data.pdf", format="pdf", bbox_inches="tight"
            )
        plt.show()

        # Task 3
        sn.lineplot(
            x="time",
            y="value",
            hue="variable",
            data=self.statistics.df_npop2,
        )
        plt.show()

        # Task 5
        plt.bar(self.statistics.x, self.statistics.out_dist)
        plt.xticks(self.statistics.x, ("x", "y", "z"))
        if self.savepdf:
            plt.savefig("task5_out.pdf", format="pdf", bbox_inches="tight")
        plt.show()

    def statistics_out(self):
        """
        Possibly write output files (expect for plots) for statistics.

        The output files are:
            - task4_out.csv
            - task5_out.npy
        """
        if self.write_out:
            # Task 4:
            self.statistics.corr2.to_csv("task4_out.csv")

            # Task 5:
            np.save("task5_out.npy", self.statistics.out_dist)

    def plot_numerics(self):
        """
        Plot all numerics plots. Possibly save them.

        The plots will be displayed in the main notebook. Depending on
        the flag savepdf, the plots are also saved to pdf files.
        """

        # Task 1
        data = self.numerics.efield_data
        for i in range(0, data.shape[1]):
            plt.figure(i)
            # plt.plot(data[:, 0], data[:, i])
            plt.plot(self.numerics.efield_time, data[:, i])
            plt.title("Column {:3d}".format(i))
            plt.show()

        # Task 2
        for i in range(self.numerics.fcols.shape[1]):
            plt.figure(i)
            plt.plot(self.numerics.freq, self.numerics.fcols[:, i])
            plt.title("RFFT Column {:3d}".format(i + 1))
            if self.savepdf:
                plt.savefig("RFFT-{:03}.pdf".format(i + 1))
            plt.show()

        # Task 4
        time = self.numerics.nstate_time
        autocorr = self.numerics.autocorr
        plt.plot(time, np.real(autocorr))
        plt.plot(time, np.imag(autocorr))
        plt.plot(time, np.abs(autocorr))
        plt.legend({"Re", "Im", "Abs"})
        if self.savepdf:
            plt.savefig("Autocorr.pdf")
        plt.show()

        # Task 6
        freq = self.numerics.freq2
        fcols = self.numerics.fcols2
        plt.plot(freq[freq > 0.0], np.abs(fcols[freq > 0.0]) ** 2)
        plt.show()
