import pytest
import numpy as np
from models import connectivity

def test_gnn_connectivity():
    """Tests GNN-based connectivity analysis."""
    eeg_data = np.random.rand(4, 1000)
    sfreq = 256
    result = connectivity.gnn_connectivity(eeg_data, sfreq)
    assert isinstance(result, float)
