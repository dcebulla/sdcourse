import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn


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
    def __init__(self, statistics, numerics, savepdf=False, write_out=False):

        self.statistics = statistics
        self.numerics = numerics
        self.savepdf = savepdf  # flag whether to save things as pdf
        self.write_out = write_out  # flag whether to write out data

    def plot_statistics(self):
        # Plot all statistic stuff

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
            data=pd.melt(self.statistics.df_npop2, ["time"]),
        )
        plt.show()

        # Task 5
        plt.bar(self.statistics.x, self.statistics.out_dist)
        plt.xticks(self.statistics.x, ("x", "y", "z"))
        if self.savepdf:
            plt.savefig("task5_out.pdf", format="pdf", bbox_inches="tight")
        plt.show()

    def statistics_out(self):
        # Write output files (expect for plots) for statistics
        if self.write_out:
            # Task 4:
            self.statistics.corr2.to_csv("task4_out.csv")

            # Task 5:
            np.save("task5_out.npy", self.statistics.out_dist)

    def plot_numerics(self):
        # Plot all numerics stuff

        # Task 1
        data = self.numerics.efield
        for i in range(1, data.shape[1]):
            plt.figure(i)
            plt.plot(data[:, 0], data[:, i])
            plt.title("Column {:3d}".format(i))
            plt.show()

        # Task 2
        for i in range(self.numerics.cols.shape[1]):
            plt.figure(i)
            plt.plot(self.numerics.freq, self.numerics.fcols[:, i])
            plt.title("RFFT Column {:3d}".format(i + 1))
            if self.savepdf:
                plt.savefig("RFFT-{:03}.pdf".format(i + 1))
            plt.show()

        # Task 4
        time = self.numerics.time
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
