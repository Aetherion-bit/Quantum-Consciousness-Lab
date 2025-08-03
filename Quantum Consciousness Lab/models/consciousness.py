import numpy as np
import pennylane as qml
from pennylane import numpy as pnp
from models.quantum import initialize_wave_packet, sample_vacuum_fluctuations
from models.optimization import optimize_frequencies

def compute_consciousness(density_matrix: list, entanglement: float, entropy: float,
                         qft_noise: float, decoherence: float) -> dict:
    """
    Computes C(t) = Φ_QM(t) * E(t) / (S_vN(t) + N_QFT(t) + Γ_dec(t)).
    Args:
        density_matrix: Flattened quantum density matrix.
        entanglement: Entanglement measure [0-1].
        entropy: Von Neumann entropy.
        qft_noise: Quantum field theory noise.
        decoherence: Decoherence rate.
    Returns:
        Dictionary with C(t) and component values.
    """
    rho = pnp.array(density_matrix).reshape((-1, -1))
    if not np.allclose(rho, rho.conj().T) or not np.allclose(np.trace(rho), 1):
        raise ValueError("Invalid density matrix")
    
    phi_qm = float(pnp.trace(rho @ rho))
    
    # Schmidt decomposition for entanglement
    _, s, _ = pnp.linalg.svd(rho)
    s = s[s > 1e-10]
    computed_entanglement = float(-np.sum(s**2 * pnp.log2(s**2)))
    entanglement = min(entanglement, computed_entanglement)
    
    s_vn = float(-np.sum(s * pnp.log2(s + 1e-10)))
    
    denominator = s_vn + qft_noise + decoherence
    if abs(denominator) < 1e-10:
        raise ValueError("Denominator near zero.")
    
    c_t = (phi_qm * entanglement) / denominator
    
    return {
        "C(t)": c_t,
        "phi_qm": phi_qm,
        "entanglement": entanglement,
        "s_vn": s_vn,
        "qft_noise": qft_noise,
        "gamma_dec": decoherence
    }

def compute_c_sigma(eeg_data: np.ndarray, sfreq: float, time_windows: int = 10) -> dict:
    """
    Computes C_Σ(t) as time-averaged C(t) with coherence optimization.
    Args:
        eeg_data: EEG data (channels x samples).
        sfreq: Sampling frequency (Hz).
        time_windows: Number of time windows for averaging.
    Returns:
        Dictionary with C_Σ(t), C(t) values, and optimized frequencies.
    """
    window_size = eeg_data.shape[1] // time_windows
    c_t_values = []
    
    for i in range(time_windows):
        window_data = eeg_data[:, i*window_size:(i+1)*window_size]
        features = analyze_eeg_band(window_data, sfreq)
        rho = np.array(features["density_matrix"]).reshape((-1, -1))
        c_t = compute_consciousness(
            rho.flatten().tolist(),
            features["connectivity_wpli"],
            features["entropy"],
            features["qft_noise"],
            features["decoherence"]
        )["C(t)"]
        c_t_values.append(c_t)
    
    opt_freqs = optimize_frequencies(eeg_data, sfreq)
    c_sigma = float(np.mean(c_t_values))
    
    return {
        "C_sigma(t)": c_sigma,
        "C(t)_values": c_t_values,
        "optimized_frequencies": opt_freqs
      }
