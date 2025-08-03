import pytest
import numpy as np
from models import bci

def test_connect_bci():
    """Tests BCI connection (mocked)."""
    board = bci.connect_bci()
    assert board is not None

def test_analyze_bci_data():
    """Tests BCI data analysis with mock data."""
    bci_data = np.random.rand(4, 1000)
    sfreq = 256
    result = bci.analyze_bci_data(bci_data, sfreq)
    assert "band_power" in result
    assert "connectivity_wpli" in result
