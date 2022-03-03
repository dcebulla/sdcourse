import numpy as np


class Numerics:
    def __init__(self, efield, nstate, threshold):
        self.efield_time, self.efield_data = efield[:, 0], self._rm_blw_thrsh(
            efield[:, 1:], threshold
        )
        self.nstate_time, self.nstate_data = (
            nstate[:, 0],
            nstate[:, 1::2] + 1j * nstate[:, 2::2],
        )

    def run(self):
        self.compute_rfft()
        self.compute_autocorrelation()
        self.compute_fft()

    def compute_rfft(self):
        n = self.efield_data.shape[0]
        self.fcols = np.fft.rfft(self.efield_data, axis=0)
        self.freq = np.fft.rfftfreq(n)

    def compute_autocorrelation(self):
        cmplx_data = self.nstate_data
        autocorr = np.zeros(cmplx_data.shape[0], dtype=np.complex)
        for i in range(cmplx_data.shape[0]):
            autocorr[i] = np.sum(cmplx_data[0, :] * np.conj(cmplx_data[i, :]))
        self.autocorr = autocorr

    def compute_fft(self):
        n = self.autocorr.size
        self.fcols2 = np.fft.fft(self.autocorr)
        self.freq2 = np.fft.fftfreq(n)

    def _rm_blw_thrsh(self, a, tol=1e-6):
        return a[:, np.var(a, axis=0) > tol]
