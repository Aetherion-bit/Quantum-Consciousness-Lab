import mne
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html
from scipy.integrate import odeint
from sklearn.decomposition import PCA
from models.eeg import analyze_eeg_band

def visualize_eeg(eeg_data, sfreq):
    """
    Visualizes EEG time series.
    """
    raw = mne.io.RawArray(eeg_data, mne.create_info(len(eeg_data), sfreq, ch_types='eeg'))
    fig = go.Figure()
    for i, channel in enumerate(raw.get_data()):
        fig.add_trace(go.Scatter(y=channel, name=f"Channel {i+1}"))
    fig.update_layout(title="EEG Time Series", xaxis_title="Time", yaxis_title="Amplitude")
    return fig

def compute_attractor(eeg_data: np.ndarray, sfreq: float) -> dict:
    """
    Computes Lorenz and PCA attractors with Lyapunov exponent.
    """
    def lorenz(state, t, sigma=10, rho=28, beta=8/3):
        x, y, z = state
        return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]
    
    features = analyze_eeg_band(eeg_data, sfreq)
    initial_state = [features["band_power"]["theta"], features["connectivity_wpli"], features["entropy"]]
    t = np.linspace(0, 10, 1000)
    trajectory = odeint(lorenz, initial_state, t)
    
    data = np.array([features["band_power"][band] for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']] + [features["connectivity_wpli"], features["entropy"]])
    pca = PCA(n_components=3)
    pca_trajectory = pca.fit_transform(np.repeat(data.reshape(1, -1), 1000, axis=0))
    
    lyapunov = compute_lyapunov_exponent(trajectory)
    return {"lorenz": trajectory, "pca": pca_trajectory, "lyapunov": lyapunov}

def compute_lyapunov_exponent(trajectory: np.ndarray, dt: float = 0.01) -> float:
    """
    Computes the largest Lyapunov exponent.
    """
    def lorenz(state, t):
        sigma, rho, beta = 10, 28, 8/3
        x, y, z = state
        return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]
    
    n = len(trajectory)
    divergence = 0
    for i in range(n - 1):
        state = trajectory[i]
        perturbed = state + np.random.normal(0, 1e-5, 3)
        next_state = odeint(lorenz, state, [0, dt])[-1]
        next_perturbed = odeint(lorenz, perturbed, [0, dt])[-1]
        divergence += np.log(np.linalg.norm(next_perturbed - next_state) / 1e-5)
    return divergence / (n * dt)

def visualize_attractor(trajectory: dict):
    """
    Visualizes Lorenz and PCA attractors.
    """
    lorenz_fig = go.Figure(data=[
        go.Scatter3d(
            x=trajectory["lorenz"][:, 0], y=trajectory["lorenz"][:, 1], z=trajectory["lorenz"][:, 2],
            mode='lines', name='Lorenz Attractor'
        )
    ])
    lorenz_fig.update_layout(title=f"Lorenz Attractor (Lyapunov: {trajectory['lyapunov']:.2f})", scene=dict(xaxis_title="Theta", yaxis_title="WPLI", zaxis_title="Entropy"))
    
    pca_fig = go.Figure(data=[
        go.Scatter3d(
            x=trajectory["pca"][:, 0], y=trajectory["pca"][:, 1], z=trajectory["pca"][:, 2],
            mode='lines', name='PCA Attractor'
        )
    ])
    pca_fig.update_layout(title="PCA Attractor", scene=dict(xaxis_title="PC1", yaxis_title="PC2", zaxis_title="PC3"))
    
    return lorenz_fig, pca_fig

def visualize_entropy(data: dict):
    """
    Visualizes C(t) and entropy dynamics.
    """
    fig = go.Figure(data=[
        go.Scatter(x=list(range(len(data["C(t)_values"]))), y=data["C(t)_values"], mode='lines', name='C(t)')
    ])
    fig.update_layout(title="C(t) and Entropy Dynamics", xaxis_title="Time Window", yaxis_title="Value")
    return fig

def visualize_decomposition(data: dict):
    """
    Visualizes FFT and wavelet decompositions.
    """
    fft_fig = go.Figure(data=[
        go.Scatter(x=data["fft_frequencies"], y=data["fft_power"][0], name="FFT Power")
    ])
    wavelet_fig = go.Figure(data=[
        go.Heatmap(z=data["wavelet_coeffs"], x=list(range(len(data["wavelet_coeffs"][0]))), y=data["wavelet_frequencies"], name="Wavelet")
    ])
    return fft_fig, wavelet_fig

def create_dashboard(data: dict, eeg_data: np.ndarray, sfreq: float):
    """
    Creates a Dash dashboard for visualizations.
    """
    app = Dash(__name__)
    eeg_fig = visualize_eeg(eeg_data, sfreq)
    lorenz_fig, pca_fig = visualize_attractor(compute_attractor(eeg_data, sfreq))
    entropy_fig = visualize_entropy(data)
    fft_fig, wavelet_fig = visualize_decomposition(data)
    
    app.layout = html.Div([
        html.H1("Quantum Consciousness Dashboard"),
        dcc.Graph(figure=eeg_fig),
        dcc.Graph(figure=lorenz_fig),
        dcc.Graph(figure=pca_fig),
        dcc.Graph(figure=entropy_fig),
        dcc.Graph(figure=fft_fig),
        dcc.Graph(figure=wavelet_fig)
    ])
    app.run_server(debug=True)
