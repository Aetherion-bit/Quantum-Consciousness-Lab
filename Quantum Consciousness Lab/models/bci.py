from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import numpy as np

def connect_bci(board_id: int = BoardIds.SYNTHETIC_BOARD.value):
    """
    Connects to a BCI device.
    """
    params = BrainFlowInputParams()
    board = BoardShim(board_id, params)
    board.prepare_session()
    return board

def analyze_bci_data(bci_data: np.ndarray, sfreq: float) -> dict:
    """
    Analyzes BCI data using EEG pipeline.
    """
    from models.eeg import analyze_eeg_band
    return analyze_eeg_band(bci_data, sfreq)
