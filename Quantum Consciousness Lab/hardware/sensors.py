from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import numpy as np

def connect_eeg_device(board_id: int = BoardIds.SYNTHETIC_BOARD.value):
    """
    Connects to an EEG/BCI device.
    """
    params = BrainFlowInputParams()
    board = BoardShim(board_id, params)
    board.prepare_session()
    return board

def stream_eeg(board, duration: float = 10.0):
    """
    Streams EEG data from a device.
    """
    board.start_stream()
    data = board.get_board_data(int(duration * board.get_sampling_rate(board.board_id)))
    board.stop_stream()
    return data
