import numpy as np
from models.consciousness import compute_c_sigma

def initialize_tms(device_id: str = "neuroelectrics"):
    """
    Initializes TMS device.
    """
    return {"device_id": device_id, "status": "connected"}

def apply_tms_feedback(eeg_data: np.ndarray, sfreq: float):
    """
    Applies TMS pulses based on C_Σ(t).
    """
    c_sigma = compute_c_sigma(eeg_data, sfreq)["C_sigma(t)"]
    frequency = 10.0 if c_sigma < 0.5 else 20.0
    amplitude = 0.1 * c_sigma
    return {"frequency": frequency, "amplitude": amplitude}
