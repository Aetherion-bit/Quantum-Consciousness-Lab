import pytest
import numpy as np
from models import ml

def test_classify_eeg():
    """Tests EEG classification."""
    eeg_data = np.random.rand(4, 1000)
    sfreq = 256
    result = ml.classify_eeg(eeg_data, sfreq)
    assert "prediction" in result
    assert "probabilities" in result
    assert "classes" in result

def test_classify_emotion():
    """Tests emotion classification."""
    eeg_data = np.random.rand(4, 1000)
    sfreq = 256
    result = ml.classify_emotion(eeg_data, sfreq)
    assert "emotion" in result
    assert "classes" in result

def test_hybrid_classifier():
    """Tests hybrid QNN-XGBoost classifier."""
    eeg_data = np.random.rand(4, 1000)
    sfreq = 256
    result = ml.hybrid_classifier(eeg_data, sfreq)
    assert "prediction" in result
    assert "probabilities" in result
