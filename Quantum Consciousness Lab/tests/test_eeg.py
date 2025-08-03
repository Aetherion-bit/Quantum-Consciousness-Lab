import pytest
import numpy as np
from models.eeg import analyze_eeg_band

def test_analyze_eeg_band():
    eeg_data = np.random.rand(4, 1000)
    sfreq = 256
    result = analyze_eeg_band(eeg_data, sfreq)
    assert "band_power" in result
    assert len(result["fft_frequencies"]) > 0
