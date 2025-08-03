import pytest
import numpy as np
from models.quantum import initialize_wave_packet

def test_initialize_wave_packet():
    eeg_data = np.random.rand(4, 1000)
    sfreq = 256
    result = initialize_wave_packet(eeg_data, sfreq)
    assert "density_matrix" in result
    rho = np.array(result["density_matrix"])
    assert np.allclose(np.trace(rho), 1)
