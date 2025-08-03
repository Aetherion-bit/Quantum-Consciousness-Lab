import time
import numpy as np
from models.eeg import analyze_eeg_band

def test_benchmark_eeg_processing():
    eeg_data = np.random.rand(4, 1000)
    sfreq = 256
    start = time.time()
    analyze_eeg_band(eeg_data, sfreq)
    assert time.time() - start < 1.0
