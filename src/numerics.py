# -*- coding: utf-8 -*-
"""Provides functionality for numerical data analysis."""


import numpy as np


class NumericsClass:
    """Class that encapsulates methods for the numerical data analysis.

    Attributes:
        efield_time (:obj:`numpy.ndarray`): Time of efield data.
        efield_data (:obj:`numpy.ndarray`): Actual efield data.
        nstate_time (:obj:`numpy.ndarray`): Time of nstate_i data.
        nstate_data (:obj:`numpy.ndarray`): Actual complex nstate_i data.
        fcols (:obj:`numpy.ndarray`): Fourier transform of `efield_data`.
        freq (:obj:`numpy.ndarray`): Frequency  of `efield_data`.
        autocorr (:obj:`numpy.ndarray`): Autocorrelation of `nstate_data`.
        fcols2 (:obj:`numpy.ndarray`): Fourier transform of `autocorr`.
        freq2 (:obj:`numpy.ndarray`): Frequency of FFT for `autocorr`.

    """

    def __init__(self, data, threshold):
        """Initializes the class with required data.

        Args:
            data (:obj:`InClass`): Input data class.
            threshold (float): Threshold to choose significant data.

        """

        # Extract efield data
        efield = np.copy(data.efield)
        nstate = np.copy(data.nstate_i)
        self.efield_time, self.efield_data = efield[:, 0], self._rm_blw_thrsh(
            efield[:, 1:], threshold
        )

        # Extract and set up nstate_i data
        self.nstate_time, self.nstate_data = (
            nstate[:, 0],
            nstate[:, 1::2] + 1j * nstate[:, 2::2],
        )

    def run(self):
        """Runs FFTs and computes autocorrelation."""
        self.compute_rfft()
        self.compute_autocorrelation()
        self.compute_fft()

    def compute_rfft(self):
        """Computes real FFT for `efield_data`."""
        n = self.efield_data.shape[0]
        self.fcols = np.fft.rfft(self.efield_data, axis=0)
        self.freq = np.fft.rfftfreq(n)

    def compute_autocorrelation(self):
        """Computes autocorrelation of `nstate_data`."""
        cmplx_data = self.nstate_data
        autocorr = np.zeros(cmplx_data.shape[0], dtype=np.complex)
        for i in range(cmplx_data.shape[0]):
            autocorr[i] = np.sum(cmplx_data[0, :] * np.conj(cmplx_data[i, :]))
        self.autocorr = autocorr

    def compute_fft(self):
        """Computes complex FFT for `autocorr` (autocorrelation)."""
        n = self.autocorr.size
        self.fcols2 = np.fft.fft(self.autocorr)
        self.freq2 = np.fft.fftfreq(n)

    def _rm_blw_thrsh(self, a, tol=1e-6):
        """Removes columns whose variance is below threshold.

        Args:
            a (:obj:`numpy.ndarray`): Data whose columns are investigated.
            tol (float): Threshold > 0
        """
        if tol <= 0.0:
            return a

        return a[:, np.var(a, axis=0) > tol]
