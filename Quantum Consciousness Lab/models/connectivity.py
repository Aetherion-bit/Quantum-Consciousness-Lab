import torch
import torch_geometric.nn as gnn
from models.eeg import analyze_eeg_band
import numpy as np

def gnn_connectivity(eeg_data: np.ndarray, sfreq: float) -> float:
    """
    Computes connectivity using GNNs.
    """
    features = analyze_eeg_band(eeg_data, sfreq)
    wpli = np.array(features["connectivity_wpli"])
    
    edge_index = torch.tensor([[i, j] for i in range(wpli.shape[0]) for j in range(wpli.shape[1]) if wpli[i, j] > 0], dtype=torch.long).t()
    x = torch.tensor(list(features["band_power"].values()), dtype=torch.float)
    data = torch_geometric.data.Data(x=x, edge_index=edge_index)
    
    model = gnn.GCNConv(in_channels=5, out_channels=1)
    return model(data.x, data.edge_index).mean().item()
