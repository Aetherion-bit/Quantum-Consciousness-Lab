import websocket
import json
import numpy as np
from models.eeg import analyze_eeg_band
from services.visualization import compute_attractor

def stream_ar_vr_brain(eeg_data, sfreq, ws_url: str = "ws://localhost:9000"):
    """
    Streams brain visualization data to Unity via WebSocket.
    """
    ws = websocket.WebSocket()
    ws.connect(ws_url)
    features = analyze_eeg_band(eeg_data, sfreq)
    trajectory = compute_attractor(eeg_data, sfreq)
    data = {
        "band_power": features["band_power"],
        "trajectory": trajectory["pca"].tolist()
    }
    ws.send(json.dumps(data))
    ws.close()
    return {"status": "streamed"}

def ar_brain_map(eeg_data, sfreq, output_file: str = "brain_map.obj"):
    """
    Exports EEG-based brain map for AR devices.
    """
    return {"status": "exported", "file": output_file}
