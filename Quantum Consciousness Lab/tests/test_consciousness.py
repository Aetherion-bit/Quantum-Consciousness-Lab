import pytest
import numpy as np
from models.consciousness import compute_consciousness, compute_c_sigma

def test_compute_consciousness():
    rho = np.diag([0.25, 0.25, 0.25, 0.25]).flatten().tolist()
    result = compute_consciousness(rho, 0.5, 0.1, 0.1, 0.1)
    assert "C(t)" in result
    assert result["C(t)"] > 0

def test_compute_c_sigma():
    eeg_data = np.random.rand(4, 1000)
    sfreq = 256
    result = compute_c_sigma(eeg_data, sfreq)
    assert "C_sigma(t)" in result
    assert len(result["C(t)_values"]) == 10
