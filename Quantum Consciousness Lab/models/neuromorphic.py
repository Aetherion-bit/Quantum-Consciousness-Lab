from nxsdk.api.n2a import Loihi2
import numpy as np
from models.eeg import analyze_eeg_band

def neuromorphic_simulation(eeg_data: np.ndarray, sfreq: float) -> dict:
    """
    Simulates EEG data on neuromorphic hardware.
    """
    features = analyze_eeg_band(eeg_data, sfreq)
    spikes = np.array([features["band_power"][band] for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']])
    
    chip = Loihi2()
    network = chip.create_network()
    for i, spike_rate in enumerate(spikes):
        neuron = network.create_neuron(spike_rate=spike_rate * 100)
    network.run(1000)
    return {"spike_rates": spikes.tolist()}
