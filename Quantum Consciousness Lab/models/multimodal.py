import nibabel as nib
import numpy as np

def integrate_fmri(fmri_file: str, eeg_data: np.ndarray) -> dict:
    """
    Integrates fMRI data with EEG.
    """
    fmri = nib.load(fmri_file).get_fdata()
    fmri_features = np.mean(fmri, axis=(0, 1, 2))
    return {"fmri_features": fmri_features.tolist(), "eeg_data": eeg_data.tolist()}
