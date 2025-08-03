import pytest
import numpy as np
from models import optimization

def test_optimize_frequencies():
    """Tests frequency optimization."""
    eeg_data = np.random.rand(4, 1000)
    sfreq = 256
    result = optimization.optimize_frequencies(eeg_data, sfreq, n_iterations=10)
    assert "f1" in result
    assert "f2" in result
    assert isinstance(result["f1"], float)

def test_stabilize_coherence():
    """Tests PPO-based coherence stabilization."""
    eeg_data = np.random.rand(4, 1000)
    sfreq = 256
    result = optimization.stabilize_coherence(eeg_data, sfreq)
    assert "optimized_f1" in result
    assert "optimized_f2" in result

def test_stabilize_coherence_dqn():
    """Tests DQN-based coherence stabilization."""
    eeg_data = np.random.rand(4, 1000)
    sfreq = 256
    result = optimization.stabilize_coherence_dqn(eeg_data, sfreq)
    assert "optimized_f1" in result
    assert "optimized_f2" in result

def test_qaoa_feedback():
    """Tests QAOA feedback."""
    eeg_data = np.random.rand(4, 1000)
    sfreq = 256
    result = optimization.qaoa_feedback(eeg_data, sfreq)
    assert "optimized_params" in result
