import pytest
import numpy as np
from models import multimodal

def test_integrate_fmri():
    """Tests fMRI and EEG integration with mock data."""
    eeg_data = np.random.rand(4, 1000)
    fmri_file = "mock_fmri.nii"
    result = multimodal.integrate_fmri(fmri_file, eeg_data)
    assert "fmri_features" in result
    assert "eeg_data" in result
