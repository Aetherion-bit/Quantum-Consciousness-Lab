import mne
import numpy as np
from mne.preprocessing import ICA
from mne_connectivity import spectral_connectivity
from scipy.fft import fft, fftfreq
from scipy.signal import hilbert
import pywt
import tensorly as tl
import tensorly.decomposition
import torch
import torch.nn as nn

class EEGCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(4, 16, kernel_size=3)
        self.fc = nn.Linear(16 * 998, 4 * 1000)
    
    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = x.view(x.size(0), -1)
        return self.fc(x)

def analyze_eeg_band(eeg_data: np.ndarray, sfreq: float) -> dict:
    """
    Analyzes EEG data with FFT, wavelet, Hilbert, tensor decomposition, and CNN artifact correction.
    Args:
        eeg_data: EEG data (channels x samples).
        sfreq: Sampling frequency (Hz).
    Returns:
        Dictionary with band powers, connectivity, ErrP, and decomposition results.
    """
    if not isinstance(eeg_data, np.ndarray) or eeg_data.size == 0:
        raise ValueError("Invalid EEG data")
    if sfreq <= 0:
        raise ValueError("Sampling frequency must be positive")

    info = mne.create_info(ch_names=[f'ch{i+1}' for i in range(eeg_data.shape[0])], sfreq=sfreq, ch_types='eeg')
    raw = mne.io.RawArray(eeg_data, info)

    # ICA
    ica = ICA(n_components=min(20, eeg_data.shape[0]), random_state=42)
    ica.fit(raw)
    raw_clean = ica.apply(raw.copy())

    # CNN artifact correction
    model = EEGCNN()
    eeg_tensor = torch.tensor(raw_clean.get_data(), dtype=torch.float32).unsqueeze(0)
    cleaned_data = model(eeg_tensor).squeeze().detach().numpy()

    # FFT
    n_samples = cleaned_data.shape[1]
    fft_vals = fft(cleaned_data, axis=1)
    freqs = fftfreq(n_samples, 1/sfreq)
    psd = np.abs(fft_vals)**2 / n_samples

    # Wavelet
    scales = np.arange(1, 128)
    coeffs, wavelet_freqs = pywt.cwt(cleaned_data, scales, 'morl', sampling_period=1/sfreq)

    # Hilbert
    analytic_signal = hilbert(cleaned_data, axis=1)
    amplitude = np.abs(analytic_signal)
    phase = np.angle(analytic_signal)
    phase_sync = float(np.mean(np.cos(phase[:, :, None] - phase[:, None, :])))

    # Tensor decomposition
    tensor = tl.tensor(cleaned_data)
    factors = tl.decomposition.parafac(tensor, rank=3)

    bands = {
        'delta': (1, 4),
        'theta': (4, 8),
        'alpha': (8, 12),
        'beta': (12, 30),
        'gamma': (30, 100)
    }
    band_power = {}
    wavelet_power = {}
    for band, (low, high) in bands.items():
        fft_idx = np.logical_and(freqs >= low, freqs <= high)
        wavelet_idx = np.logical_and(wavelet_freqs >= low, wavelet_freqs <= high)
        band_power[band] = float(np.mean(psd[:, fft_idx]))
        wavelet_power[band] = float(np.mean(np.abs(coeffs[wavelet_idx])**2))

    # WPLI
    con, _, _, _, _ = spectral_connectivity(raw_clean, method='wpli', fmin=1, fmax=100)
    connectivity = float(np.mean(con))

    # ErrP
    time_window = int(0.2 * sfreq), int(0.5 * sfreq)
    errp_data = raw_clean.get_data()[:, time_window[0]:time_window[1]]
    errp_fft = fft(errp_data, axis=1)
    errp_freqs = fftfreq(errp_data.shape[1], 1/sfreq)
    errp_idx = np.logical_and(errp_freqs >= 4, errp_freqs <= 8)
    errp_power = float(np.mean(np.abs(errp_fft[:, errp_idx])**2))

    # Density matrix
    band_values = np.array([band_power[band] for band in bands])
    rho = np.diag(band_values / np.sum(band_values))
    s_vn = -np.sum(band_values * np.log2(band_values + 1e-10)) / np.sum(band_values)

    return {
        "band_power": band_power,
        "wavelet_power": wavelet_power,
        "connectivity_wpli": connectivity,
        "errp_power": errp_power,
        "density_matrix": rho.flatten().tolist(),
        "entropy": s_vn,
        "qft_noise": float(np.std(psd)),
        "decoherence": float(np.var(con)),
        "fft_frequencies": freqs.tolist(),
        "fft_power": psd.tolist(),
        "wavelet_coeffs": coeffs.tolist(),
        "wavelet_frequencies": wavelet_freqs.tolist(),
        "phase_sync": phase_sync,
        "tensor_factors": [f.tolist() for f in factors[1]]
      }
