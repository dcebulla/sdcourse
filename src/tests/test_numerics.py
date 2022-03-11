import numpy as np
from numerics import NumericsClass


# Define own data class to pass to NumericsClass
class TmpData:
    def __init__(self, tol):
        self.efield = np.array(
            [
                [0.0, 0.0, 10 * np.sqrt(tol), 3.0],
                [1.0, tol / 2, 5 * np.sqrt(tol), 1.0],
                [2.0, tol / 2, np.sqrt(tol), 1.0],
            ]
        )
        self.nstate_i = np.array(
            [[0.0, 1.0, 2.0], [1.0, 3.0, 4.0], [2.0, 5.0, 6.0]]
        )


tol = 1e-5
data = TmpData(tol)
nums = NumericsClass(data, tol)


def test_threshold():
    # Check if removal of columns based on threshold works
    a = data.efield[:, 1:]
    b = nums._rm_blw_thrsh(a, tol)
    c = nums._rm_blw_thrsh(a, -tol)  # Array unchanged when tol <= 0
    assert a[:, [1, 2]].shape == b.shape
    assert np.all(np.isclose(a[:, [1, 2]], b))
    assert np.all(np.isclose(a, c))


def test_cmplx_data():
    # Check if transform to complex numbers works
    assert np.all(
        np.isclose(
            nums.nstate_data.flatten(),
            (data.nstate_i[:, 1] + 1j * data.nstate_i[:, 2]).flatten(),
        )
    )
