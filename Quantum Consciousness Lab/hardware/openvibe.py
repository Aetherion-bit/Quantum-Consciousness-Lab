from pythonosc import udp_client
import numpy as np

def connect_openvibe(ip: str = "127.0.0.1", port: int = 5678):
    """
    Connects to OpenVibe for EEG streaming.
    """
    return udp_client.SimpleUDPClient(ip, port)

def stream_openvibe_eeg(client, duration: float = 10.0, sfreq: float = 256):
    """
    Streams EEG data from OpenVibe.
    """
    return np.random.rand(4, int(duration * sfreq))  # Placeholder
